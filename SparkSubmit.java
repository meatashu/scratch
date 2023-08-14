import java.io.IOException;
import java.util.Arrays;
import java.util.Scanner;

public class SparkSubmit {

    public static void main(String[] args) throws IOException {
        // Get the user input
        Scanner scanner = new Scanner(System.in);

        // Get the optional Spark submit parameters
        System.out.println("Enter the Spark jar path (leave blank to use default): ");
        String jarPath = scanner.nextLine();
        System.out.println("Enter the Spark master URL (leave blank to use default): ");
        String masterUrl = scanner.nextLine();
        System.out.println("Enter the Spark application name (leave blank to use default): ");
        String appName = scanner.nextLine();
        System.out.println("Enter the Spark application arguments (leave blank to use default): ");
        String[] appArgs = scanner.nextLine().split(" ");

        // Set the default Spark submit parameters
        String defaultJarPath = "/path/to/spark/jar";
        String defaultMasterUrl = "local[4]";
        String defaultAppName = "MySparkApplication";
        String[] defaultAppArgs = {};

        // Substitute the default values for the optional parameters that were left blank
        if (jarPath.isEmpty()) {
            jarPath = defaultJarPath;
        }
        if (masterUrl.isEmpty()) {
            masterUrl = defaultMasterUrl;
        }
        if (appName.isEmpty()) {
            appName = defaultAppName;
        }
        if (appArgs.length == 0) {
            appArgs = defaultAppArgs;
        }

        // Build the Spark submit command
        String sparkSubmitCommand = "spark-submit";
        sparkSubmitCommand += " --master " + masterUrl;
        sparkSubmitCommand += " --class " + appName;
        sparkSubmitCommand += " " + jarPath;
        sparkSubmitCommand += " " + Arrays.toString(appArgs);

        // Execute the Spark submit command
        System.out.println("Executing Spark submit command: " + sparkSubmitCommand);
        Process process = Runtime.getRuntime().exec(sparkSubmitCommand);
        process.waitFor();


        // Check the exit code
        int exitCode = process.exitValue();
        if (exitCode != 0) {
            System.out.println("Spark submit failed with exit code " + exitCode);
        } else {
            System.out.println("Spark submit succeeded");
        }

        // Get the spark application id and status
        String sparkApplicationId = getSparkApplicationId(process.getInputStream());
        String sparkApplicationStatus = getSparkApplicationStatus(process.getInputStream());

        // Print the spark application id and status
        System.out.println("Spark application id: " + sparkApplicationId);
        System.out.println("Spark application status: " + sparkApplicationStatus);

                // Check the spark application status every 60 seconds
        while (!sparkApplicationStatus.equals("FINISHED")) {
            Thread.sleep(60000);
            sparkApplicationStatus = getSparkApplicationStatus(process.getInputStream());
        }

        // Print the spark application status
        System.out.println("Spark application status: " + sparkApplicationStatus);
    }

    private static String getSparkApplicationId(InputStream inputStream) throws IOException {
        String sparkApplicationId = "";
        String line;
        while ((line = readLine(inputStream)) != null) {
            if (line.contains("Spark application ID: ")) {
                sparkApplicationId = line.split(" ")[2];
                break;
            }
        }
        return sparkApplicationId;
    }

    private static String getSparkApplicationStatus(InputStream inputStream) throws IOException {
        String sparkApplicationStatus = "";
        String line;
        while ((line = readLine(inputStream)) != null) {
            if (line.contains("Spark application status: ")) {
                sparkApplicationStatus = line.split(" ")[2];
                break;
            }
        }
        return sparkApplicationStatus;
    }

    private static String readLine(InputStream inputStream) throws IOException {
        byte[] bytes = new byte[1024];
        int read = inputStream.read(bytes);
        if (read == -1) {
            return null;
        }
        return new String(bytes, 0, read);
    }
}
