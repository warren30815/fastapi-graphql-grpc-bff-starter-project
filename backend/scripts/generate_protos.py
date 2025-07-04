import subprocess
import os

def generate_protos():
    proto_dir = "protos"
    output_dir = "generated"
    proto_files = [os.path.join(proto_dir, f) for f in os.listdir(proto_dir) if f.endswith('.proto')]
    os.makedirs(output_dir, exist_ok=True)

    for proto_file in proto_files:
        cmd = [
            "python", "-m", "grpc_tools.protoc",
            f"-I{output_dir}={proto_dir}",
            f"--python_out=.",
            f"--grpc_python_out=.",
            proto_file
        ]

        print(f"Generating {proto_file}...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error generating {proto_file}: {result.stderr}")
            return False

        print(f"{proto_file} generated successfully!")

    return True


if __name__ == "__main__":
    generate_protos()
