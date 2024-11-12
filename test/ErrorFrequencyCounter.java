import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class ErrorFrequencyCounter {
    public static void main(String[] args) {

        CsvFileGenerator.main(new String[] { "" });
        String filePath = "generated_data.csv";
        Map<String, Integer> errorFrequency = new HashMap<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            br.readLine();
            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                if (values.length > 0) {
                    String description = values[values.length - 1].trim();
                    errorFrequency.put(description, errorFrequency.getOrDefault(description, 0) + 1);
                }
            }
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }
        System.out.println("\n=== Error Frequency Report ===\n");
        System.out.printf("%-40s %10s\n", "Error Description", "Frequency");
        System.out.println("=".repeat(52));
        for (Map.Entry<String, Integer> entry : errorFrequency.entrySet()) {
            System.out.printf("%-40s %10d\n", entry.getKey(), entry.getValue());
        }
    }
}
