import java.io.File;
import java.util.jar.JarFile;
import java.util.jar.Manifest;

public class JarValidator {

    public static void main(String[] args) throws Exception {
        String jarPath = args[0];
        JarFile jarFile = new JarFile(jarPath);
        Manifest manifest = jarFile.getManifest();

        // Get the list of dependencies from the manifest.
        String[] dependencies = manifest.getMainAttributes().getValue("Dependencies").split(",");

        // Check if all dependencies are from a RELEASE version.
        for (String dependency : dependencies) {
            String version = dependency.split(":")[1];
            if (version.endsWith("-SNAPSHOT")) {
                throw new Exception("The jar contains a snapshot dependency: " + dependency);
            }
        }

        System.out.println("The jar contains all dependencies from a RELEASE version and no snapshot versions.");
    }
}
