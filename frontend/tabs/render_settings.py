import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import hashlib
import time

CORRECT_PIN_HASH = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"  
# This is hash for PIN = 123456
MAX_ATTEMPTS = 3
LOCKOUT_TIME = 300  # 5 minutes in seconds

def verify_pin(pin):
    """Verify PIN with protection against timing attacks"""
    if not pin.isdigit() or len(pin) != 6:
        return False
    hashed_input = hashlib.sha256(pin.encode()).hexdigest()
    # return st.secrets.compare_digest(hashed_input, CORRECT_PIN_HASH)
    return hashed_input == CORRECT_PIN_HASH

def render_pin_interface():
    """Render the PIN entry interface with animations"""
    st.markdown("""
        <style>
        .locked-container {
            text-align: center;
            padding: 2rem;
            animation: fadeIn 0.5s ease-in;
        }
        .pin-input {
            max-width: 200px;
            margin: 0 auto;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="locked-container">', unsafe_allow_html=True)
        # st.image("🔒", width=64)  # You can replace this with a actual lock image
        st.markdown("### Settings are locked")
        st.markdown("Enter 6-digit PIN to access settings")
        
        # PIN input with custom styling
        pin = st.text_input("PIN", type="password", max_chars=6, key="pin_input", 
                           help="Enter a 6-digit PIN", label_visibility="collapsed")
        
        if st.button("Unlock"):
            attempts = st.session_state.get('pin_attempts', 0)
            last_attempt = st.session_state.get('last_attempt_time', 0)
            
            # Check if user is in lockout period
            if time.time() - last_attempt < LOCKOUT_TIME and attempts >= MAX_ATTEMPTS:
                remaining = int(LOCKOUT_TIME - (time.time() - last_attempt))
                st.error(f"Too many attempts. Please wait {remaining} seconds.")
                return False
            
            if verify_pin(pin):
                st.session_state.settings_unlocked = True
                st.session_state.pin_attempts = 0
                st.success("Settings unlocked!")
                time.sleep(0.5)  # Small delay for animation
                st.rerun()
            else:
                attempts += 1
                st.session_state.pin_attempts = attempts
                st.session_state.last_attempt_time = time.time()
                remaining = MAX_ATTEMPTS - attempts
                
                if remaining > 0:
                    st.error(f"Incorrect PIN. {remaining} attempts remaining.")
                else:
                    st.error(f"Account locked. Please wait {LOCKOUT_TIME} seconds.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_folder_name_settings():
    """Render the folder name configuration section"""
    # st.subheader("Folder Name Configuration")
    
    # Create a container for the current config display
    config_container = st.empty()
    
    # Function to update the current config display
    def update_config_display():
        current_config = "Current Configuration: "
        if all([st.session_state.folder_date, st.session_state.depot_name, st.session_state.coach_name]):
            current_config += f"{st.session_state.folder_date}_{st.session_state.depot_name}_{st.session_state.coach_name}"
        else:
            current_config += "Not configured"
        config_container.info(current_config)
    
    # Show initial config
    update_config_display()

    # Date input
    date_value = None
    if st.session_state.folder_date:
        try:
            date_value = datetime.strptime(st.session_state.folder_date, "%d-%m-%Y")
        except:
            pass
            
    new_date = st.date_input(
        "Date",
        value=date_value,
        format="DD-MM-YYYY",
        
    )

    # Depot name input
    new_depot = st.text_input(
        "Depot Name",
        value=st.session_state.depot_name if st.session_state.depot_name else "",
    )

    # Coach name input
    new_coach = st.text_input(
        "Coach Name",
        value=st.session_state.coach_name if st.session_state.coach_name else "",
    )

    if st.button("Update Folder Configuration"):
        st.session_state.folder_date = new_date.strftime("%d-%m-%Y")
        st.session_state.depot_name = new_depot
        st.session_state.coach_name = new_coach
        update_config_display()  # Update the display immediately
        # st.experimental_rerun()  # Force a rerun to refresh the display

def load_config():
    config_path = Path(__file__).parent.parent.parent / "config.json"
    with open(config_path, "r") as f:
        return json.load(f)

def save_config(config):
    config_path = Path(__file__).parent.parent.parent / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

def get_error_descriptions(ecl_freq_summary):
    """Extract error descriptions and codes from ecl_freq_summary"""
    try:
        if ecl_freq_summary is None or ecl_freq_summary.empty:
            st.warning("No error data available. Please load data first.")
            return {}
        
        error_dict = {}
        for idx, row in ecl_freq_summary.iterrows():
            # Using the index as error code and Description column for the description
            error_dict[f"{idx} - {row['Description']}"] = idx
        return error_dict
    except Exception as e:
        st.warning(f"Error processing error descriptions: {str(e)}")
        return {}

def render_error_log_config(config):
    with st.expander("Error Log Configuration"):
        modified = False
        
        try:
            # Get error descriptions if available in session state
            error_descriptions = {}
            if 'data_handler' not in st.session_state:
                st.warning("Please load data files first to enable error code selection.")
            else:
                if not hasattr(st.session_state.data_handler, 'ecl_freq_summary'):
                    st.warning("Error log data not initialized. Please load data files.")
                else:
                    error_descriptions = get_error_descriptions(st.session_state.data_handler.ecl_freq_summary)
            
            for group, errors in config["ERROR_LOG_TAB"].items():
                st.subheader(group)
                
                # Add multiselect widget if error descriptions are available and toggle is on
                if error_descriptions and st.session_state.get('show_multiselect', True):
                    st.write("Select from available errors:")
                    # Create options list where current errors are pre-selected
                    options = list(error_descriptions.keys())
                    default = [opt for opt in options if error_descriptions[opt] in errors]
                    
                    selected = st.multiselect(
                        f"Error codes for {group} (Select from list)",
                        options=options,
                        default=default,
                        key=f"multiselect_{group}"
                    )
                    selected_codes = [error_descriptions[sel] for sel in selected]
                    
                    st.write("Or manually enter/edit error codes:")
                
                # Keep the manual text input option
                new_errors = st.text_area(
                    f"Error codes for {group} (Manual input)",
                    value=", ".join(errors),
                    help="Enter error codes separated by commas",
                    key=f"manual_{group}"
                )
                
                # Combine both inputs if multiselect was used
                if error_descriptions:
                    manual_codes = [e.strip() for e in new_errors.split(",") if e.strip()]
                    combined_codes = list(set(selected_codes + manual_codes))
                    if combined_codes != errors:
                        config["ERROR_LOG_TAB"][group] = combined_codes
                        modified = True
                else:
                    # Use only manual input if no error descriptions available
                    new_error_list = [e.strip() for e in new_errors.split(",") if e.strip()]
                    if new_error_list != errors:
                        config["ERROR_LOG_TAB"][group] = new_error_list
                        modified = True
            
        except Exception as e:
            st.error(f"Error in error log configuration: {str(e)}")
            return False
        
        return modified

def render_summary_config(config):
    with st.expander("Summary Configuration"):
        modified = False
        
        try:
            # Get error descriptions if available
            error_descriptions = {}
            if 'data_handler' not in st.session_state:
                st.warning("Please load data files first to enable error code selection.")
            else:
                if not hasattr(st.session_state.data_handler, 'ecl_freq_summary'):
                    st.warning("Summary data not initialized. Please load data files.")
                else:
                    error_descriptions = get_error_descriptions(st.session_state.data_handler.ecl_freq_summary)
            
            for section, data in config["SUMMARY_TAB"].items():
                st.subheader(section)
                
                # Handle columns
                cols = st.text_area(
                    f"Columns for {section}",
                    value=", ".join(data["COLUMNS"]),
                    help="Enter column names separated by commas"
                )
                new_cols = [c.strip() for c in cols.split(",") if c.strip()]
                if new_cols != data["COLUMNS"]:
                    config["SUMMARY_TAB"][section]["COLUMNS"] = new_cols
                    modified = True
                
                # Handle other error lists
                for key, value in data.items():
                    if key != "COLUMNS":
                        if error_descriptions and st.session_state.get('show_multiselect', True):
                            st.write(f"Select {key} from available errors:")
                            options = list(error_descriptions.keys())
                            default = [opt for opt in options if error_descriptions[opt] in value]
                            
                            selected = st.multiselect(
                                f"{key} (Select from list)",
                                options=options,
                                default=default,
                                key=f"multiselect_{section}_{key}"
                            )
                            selected_codes = [error_descriptions[sel] for sel in selected]
                            
                            st.write(f"Or manually enter/edit {key}:")
                        
                        items = st.text_area(
                            f"{key} (Manual input)",
                            value=", ".join(value),
                            help="Enter items separated by commas",
                            key=f"manual_{section}_{key}"
                        )
                        
                        if error_descriptions:
                            manual_items = [i.strip() for i in items.split(",") if i.strip()]
                            combined_items = list(set(selected_codes + manual_items))
                            if combined_items != value:
                                config["SUMMARY_TAB"][section][key] = combined_items
                                modified = True
                        else:
                            new_items = [i.strip() for i in items.split(",") if i.strip()]
                            if new_items != value:
                                config["SUMMARY_TAB"][section][key] = new_items
                                modified = True
            
        except Exception as e:
            st.error(f"Error in summary configuration: {str(e)}")
            return False
        
        return modified

def render_fill_vent_config(config):
    with st.expander("Fill/Vent Configuration"):
        modified = False
        col1, col2 = st.columns(2)
        pairs = config["FILL_VENT_PAIRS"]
        
        for (fill_key, fill_val), (vent_key, vent_val) in zip(
            list(pairs.items())[::2], list(pairs.items())[1::2]
        ):
            with col1:
                new_fill = st.text_input(f"{fill_key}", value=fill_val)
                if new_fill != fill_val:
                    pairs[fill_key] = new_fill
                    modified = True
            with col2:
                new_vent = st.text_input(f"{vent_key}", value=vent_val)
                if new_vent != vent_val:
                    pairs[vent_key] = new_vent
                    modified = True
        return modified

def render_config_settings():
    try:
        st.subheader("Configuration Settings")
        
        if "config" not in st.session_state:
            try:
                st.session_state.config = load_config()
            except Exception as e:
                st.error(f"Error loading configuration: {str(e)}")
                return
        
        config = st.session_state.config
        modified = False
        
        # Error description
        with st.expander("Error Description"):
            new_desc = st.text_input("Error Description", value=config["ERROR_DESCRIPTION"])
            if new_desc != config["ERROR_DESCRIPTION"]:
                config["ERROR_DESCRIPTION"] = new_desc
                modified = True
        
        # Render other sections
        modified |= render_error_log_config(config)
        modified |= render_summary_config(config)
        modified |= render_fill_vent_config(config)
        
        if modified and st.button("Save Configuration"):
            try:
                save_config(config)
                st.success("Configuration saved successfully!")
            except Exception as e:
                st.error(f"Error saving configuration: {str(e)}")
    
    except Exception as e:
        st.error(f"Error in configuration settings: {str(e)}")

def render_settings():
    """Main settings panel render function"""
    # Initialize session state for settings lock
    if 'settings_unlocked' not in st.session_state:
        st.session_state.settings_unlocked = False
    
    # Show lock button if settings are unlocked
    if st.session_state.settings_unlocked:
        if st.button("🔒 Lock Settings", type="secondary"):
            st.session_state.settings_unlocked = False
            st.rerun()
    
    # Show either PIN interface or settings content
    if not st.session_state.settings_unlocked:
        render_pin_interface()
        return
    
    # Original settings content
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Settings")
    with col2:
        show_multiselect = st.toggle("Show Multiselect", value=True)
        st.session_state.show_multiselect = show_multiselect
    
    # Relocated this settings to the summary tab
    # Section for folder name configuration
    # with st.expander("Folder Name Configuration", expanded=True):
    #     render_folder_name_settings()
    
    # Section for JSON configuration
    render_config_settings()
