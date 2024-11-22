def create_tab_label(self, title, icon, badge_count=None):
        """Create a formatted tab label with icon and optional badge"""
        badge_html = f'<span class="tab-badge">{badge_count}</span>' if badge_count is not None else ''
        return f"""
            <div style="display: flex; align-items: center; gap: 8px;">
                {icon} {title} {badge_html}
            </div>
        """
    