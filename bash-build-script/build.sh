#!/usr/bin/env bash

compiler="${CC:-cc}"
build_dir="build"

checked=0
successful=0
failed=0

# TODO: Create the build directory.
mkdir -p "$build_dir"

# TODO: Check whether any .c files exist.
if [ ! -e ./*.c ] 2>/dev/null; then
    echo "No .c files found in the current directory."
    exit 0
fi

for source_file in ./*.c; do
    # TODO: Get the filename without "./".
    filename="${source_file#./}"

    # TODO: Remove the .c extension.
    program_name="${filename%.c}"

    # TODO: Create the output path.
    output_file="$build_dir/$program_name"

    echo "Compiling: $filename"

    # TODO: Compile the source file.
    if $compiler -Wall -Wextra -std=c23 "$source_file" -o "$output_file"; then
        echo "SUCCESS: $filename -> $output_file"
        ((successful++))
    else
        echo "FAILURE: $filename"
        ((failed++))
    fi

    ((checked++))

    echo
done

echo "Build summary"
echo "-------------"
echo "Files checked:     $checked"
echo "Successful builds: $successful"
echo "Failed builds:     $failed"
