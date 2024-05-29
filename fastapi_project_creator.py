import os


def create_fastapi_project(project_name):
    # Define the project structure
    directories = [
        project_name,
        os.path.join(project_name, 'app'),
        os.path.join(project_name, 'app', 'routers'),
    ]

    files = [
        os.path.join(project_name, 'app', 'main.py'),
        os.path.join(project_name, 'app', 'models.py'),
        os.path.join(project_name, 'app', 'database.py'),
        os.path.join(project_name, 'app', 'schemas.py'),
        os.path.join(project_name, 'app', 'config.py'),
        os.path.join(project_name, 'app', 'oauth2.py'),
        os.path.join(project_name, 'app', 'utils.py'),
        os.path.join(project_name, '.dockerignore'),
        os.path.join(project_name, 'DockerFile'),
        os.path.join(project_name, 'docker-compose.yml'),
        os.path.join(project_name, '.env'),
    ]

    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Create files
    for file in files:
        open(file, 'w').close()


if __name__ == '__main__':
    project_name = input("Enter the project name: ")
    create_fastapi_project(project_name)
    print(f"Project structure for '{project_name}' has been created.")
