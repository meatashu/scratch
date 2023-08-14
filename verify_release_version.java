import java.io.File;
import java.util.jar.JarFile;
import java.util.jar.Manifest;
import java.util.List;
import java.util.stream.Collectors;

import org.jfrog.artifactory.client.Artifactory;
import org.jfrog.artifactory.client.ArtifactoryClientBuilder;
import org.jfrog.artifactory.client.ArtifactoryVersion;
import org.jfrog.artifactory.client.impl.ArtifactoryImpl;
import org.jfrog.artifactory.client.model.RepositoryItem;

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

        // Create an Artifactory client.
        Artifactory artifactory = new ArtifactoryImpl("https://artifactory.example.com", "admin", "password", ArtifactoryVersion.LATEST);

        // Get the latest versions of the dependencies from Artifactory.
        List<RepositoryItem> latestVersions = dependencies.stream()
            .map(dependency -> artifactory.getRepository("libs-release").getItem(dependency))
            .collect(Collectors.toList());

        // Check if the jar file is using the latest versions of the dependencies.
        for (int i = 0; i < dependencies.length; i++) {
            String dependency = dependencies[i];
            RepositoryItem latestVersion = latestVersions.get(i);

            String version = dependency.split(":")[1];
            String latestVersionString = latestVersion.getVersion();

            if (!version.equals(latestVersionString)) {
                throw new Exception("The jar contains an outdated dependency: " + dependency + " (latest version: " + latestVersionString + ")");
            }
        }

        System.out.println("The jar contains all dependencies from the latest available version.");
    }
}
