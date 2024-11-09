import click
import os


def create_project(nombre_proyecto, nombre_role, ruta='.'):
    project_path = os.path.join(ruta, nombre_proyecto)
    
    # Verificar si la carpeta principal del proyecto ya existe
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print(f"Carpeta del proyecto '{nombre_proyecto}' creada en {project_path}.")
    else:
        print(f"La carpeta del proyecto '{nombre_proyecto}' ya existe en {project_path}.")
    
    # Verificar y crear las carpetas generales si no existen
    for folder in ['group_vars', 'host_vars']:
        folder_path = os.path.join(project_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Carpeta '{folder}' creada en {folder_path}.")
        else:
            print(f"La carpeta '{folder}' ya existe en {folder_path}.")
    
    # Crear la carpeta del rol y sus subcarpetas
    role_path = os.path.join(project_path, 'roles', nombre_role)
    if not os.path.exists(role_path):
        os.makedirs(role_path)
        print(f"Carpeta del rol '{nombre_role}' creada en {role_path}.")
    
    for subfolder in ['handlers', 'meta', 'files', 'tasks', 'templates', 'vars']:
        subfolder_path = os.path.join(role_path, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
            with open(os.path.join(subfolder_path, 'main.yml'), 'w') as f:
                f.write(f"# {subfolder} main.yml for role {nombre_role}\n")
            print(f"Carpeta '{subfolder}' y el archivo 'main.yml' creados en {subfolder_path}.")
        else:
            print(f"La carpeta '{subfolder}' ya existe en {subfolder_path}.")



def create_project_nr(nombre_proyecto, ruta='.'):
    project_path = os.path.join(ruta, nombre_proyecto)
    
    # Verificar si la carpeta principal del proyecto ya existe
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print(f"Carpeta del proyecto '{nombre_proyecto}' creada en {project_path}.")
    else:
        print(f"La carpeta del proyecto '{nombre_proyecto}' ya existe en {project_path}.")
    
    # Verificar y crear las carpetas 'library', 'group_vars', y 'host_vars' si no existen
    for folder in ['library', 'group_vars', 'host_vars']:
        folder_path = os.path.join(project_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Carpeta '{folder}' creada en {folder_path}.")
        else:
            print(f"La carpeta '{folder}' ya existe en {folder_path}.")


            
def create_role(nombre_role, ruta='.'):
    role_path = os.path.join(ruta, 'roles', nombre_role)
    
    # Verificar si la carpeta del rol ya existe
    if not os.path.exists(role_path):
        os.makedirs(role_path)
        print(f"Carpeta del rol '{nombre_role}' creada en {role_path}.")
    else:
        print(f"La carpeta del rol '{nombre_role}' ya existe en {role_path}.")
    
    # Crear subcarpetas dentro del rol si no existen
    for subfolder in ['handlers', 'meta', 'files', 'tasks', 'templates', 'vars']:
        subfolder_path = os.path.join(role_path, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
            with open(os.path.join(subfolder_path, 'main.yml'), 'w') as f:
                f.write(f"# {subfolder} main.yml for role {nombre_role}\n")
            print(f"Carpeta '{subfolder}' y el archivo 'main.yml' creados en {subfolder_path}.")
        else:
            print(f"La carpeta '{subfolder}' ya existe en {subfolder_path}.")                        



@click.group()
def cli():
    """Herramienta CLI para crear estructuras de proyectos de Ansible."""
    pass

@cli.command()
@click.argument('nombre_proyecto')
@click.argument('nombre_role')
@click.option('--ruta', default='.', help='Ruta donde se creará el proyecto.')
def project(nombre_proyecto, nombre_role, ruta):
    """Crea una estructura de proyecto con rol."""
    create_project(nombre_proyecto, nombre_role, ruta)

@cli.command()
@click.argument('nombre_role')
@click.option('--ruta', default='.', help='Ruta donde se creará el rol dentro del proyecto.')
def role(nombre_role, ruta):
    """Crea una estructura para un nuevo rol dentro del proyecto."""
    create_role(nombre_role, ruta)

@cli.command()
@click.argument('nombre_proyecto')
@click.option('--ruta', default='.', help='Ruta donde se creará el proyecto sin rol.')
def projectnr(nombre_proyecto, ruta):
    """Crea un proyecto sin rol (solo library, group_vars, host_vars)."""
    create_project_nr(nombre_proyecto, ruta)

if __name__ == '__main__':
    cli()