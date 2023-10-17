#!/bin/bash

# Set the HDFS directory to scan
HDFS_DIR="/my/hdfs/directory"

# Get a list of all files and directories in the directory
FILES_AND_DIRS=$(hadoop fs -ls $HDFS_DIR)

# Iterate over the list of files and directories
for FILE_OR_DIR in $FILES_AND_DIRS; do

    # Get the file or directory size
    FILE_OR_DIR_SIZE=$(hadoop fs -stat $FILE_OR_DIR | grep -oP '(?<=Size: )\d+')

    # If the file or directory size is zero, check if it is a file or directory
    if [[ $FILE_OR_DIR_SIZE -eq 0 ]]; then

        # If the file or directory is a file, ask the user if they want to delete it
        if [[ -f $FILE_OR_DIR ]]; then

            echo "The file $FILE_OR_DIR is empty. Do you want to delete it? (y/n)"
            read CHOICE

            if [[ $CHOICE == "y" ]]; then
                hadoop fs -rm $FILE_OR_DIR
                echo "Deleted empty file: $FILE_OR_DIR"
            fi

        # If the file or directory is a directory, ask the user if they want to delete it or clean up its contents
        elif [[ -d $FILE_OR_DIR ]]; then

            echo "The directory $FILE_OR_DIR is empty. Do you want to delete it or clean up its contents? (d/c)"
            read CHOICE

            if [[ $CHOICE == "d" ]]; then
                hadoop fs -rmdir $FILE_OR_DIR
                echo "Deleted empty directory: $FILE_OR_DIR"
            elif [[ $CHOICE == "c" ]]; then

                # Clean up the directory contents
                hadoop fs -expunge $FILE_OR_DIR
                echo "Cleaned up directory contents: $FILE_OR_DIR"

            fi

        fi

    fi

done
