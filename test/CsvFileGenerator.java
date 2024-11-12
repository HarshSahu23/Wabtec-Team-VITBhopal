import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.Random;

public class CsvFileGenerator {

    public static void main(String[] args) {
        // Define CSV file path
        String filePath = "generated_data.csv";

        // Number of rows to generate
        int numRows = 50_000;

        // Generate and write the CSV file
        generateCsvFile(filePath, numRows);
    }

    private static void generateCsvFile(String filePath, int numRows) {
        String[] headers = {
                "Nr", "Code", "Ticks", "Date", "Time", "SW", "STATE", "BCU_ID", "CARS",
                "SPEED", "TPIL", "DO1", "FLAG", "TARG", "DI1", "TCF1", "TCF2", "Description"
        };

        Random random = new Random();
        DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("dd/MM/yy");
        DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("HH:mm:ss");

        try (FileWriter writer = new FileWriter(filePath)) {
            // Write header
            writer.append(String.join(",", headers)).append("\n");

            // Write rows of data
            for (int i = 1; i <= numRows; i++) {
                writer.append(String.format("%04d", i)).append(",") // Nr
                        .append("A" + String.format("%03d", random.nextInt(1000))).append(",") // Code
                        .append(String.format("%08X", random.nextInt(0xFFFFFF))).append(",") // Ticks (Hex format)
                        .append(LocalDate.now().minusDays(random.nextInt(30)).format(dateFormatter)).append(",") // Date
                        .append(LocalTime.now().minusMinutes(random.nextInt(1440)).format(timeFormatter)).append(",") // Time
                        .append(String.format("%04d", random.nextInt(10000))).append(",") // SW
                        .append(String.format("%04d", random.nextInt(10000))).append(",") // STATE
                        .append(String.format("%04d", random.nextInt(10000))).append(",") // BCU_ID
                        .append(String.format("%04d", random.nextInt(10000))).append(",") // CARS
                        .append(String.format("%04d", random.nextInt(10000))).append(",") // SPEED
                        .append(String.format("%04d", random.nextInt(10000))).append(",") // TPIL
                        .append(String.format("%04X", random.nextInt(0xFFFF))).append(",") // DO1 (Hex)
                        .append(String.format("%04X", random.nextInt(0xFFFF))).append(",") // FLAG (Hex)
                        .append(String.format("%04d", random.nextInt(10000))).append(",") // TARG
                        .append(String.format("%04d", random.nextInt(10000))).append(",") // DI1
                        .append(String.format("%04d", random.nextInt(10000))).append(",") // TCF1
                        .append(String.format("%04d", random.nextInt(10000))).append(",") // TCF2
                        .append(generateRandomDescription(random)) // Description
                        .append("\n");
            }
            System.out.println("CSV file generated at: " + filePath);
        } catch (IOException e) {
            System.out.println("Error writing file: " + e.getMessage());
        }
    }

    // Generates a random error description
    private static String generateRandomDescription(Random random) {
        String[] descriptions = {
                "I_BP_LOW", "RESET_I_BP_LOW", "POWER_ON", "I_BP_HIGH", "COMM_ERROR",
                "OVER_VOLTAGE", "UNDER_VOLTAGE", "SENSOR_FAIL", "BRAKE_ERROR", "FAULT_RESET"
        };
        return descriptions[random.nextInt(descriptions.length)];
    }
}
