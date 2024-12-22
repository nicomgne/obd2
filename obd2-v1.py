import obd
import time
## ============================================== PARAMETRES ============================================== ##

DEVELOPER_MODE = True
if DEVELOPER_MODE == False:  connection = obd.OBD(portstr='COM8')

# Définition des couleurs pour l'affichage
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"

# Dictionnaire des protocoles OBD-II
obd_protocols = {
    "1": "SAE J1850 PWM",
    "2": "SAE J1850 VPW",
    "3": "AUTO, ISO 9141-2",
    "4": "ISO 14230-4 (KWP 5BAUD)",
    "5": "ISO 14230-4 (KWP FAST)",
    "6": "ISO 15765-4 (CAN 11/500)",
    "7": "ISO 15765-4 (CAN 29/500)",
    "8": "ISO 15765-4 (CAN 11/250)",
    "9": "ISO 15765-4 (CAN 29/250)",
    "A": "SAE J1939 (CAN 29/250)"
}

# Dictionnaire des commandes disponibles
elm_info = {
    '0': None,
    '1': obd.commands.ELM_VERSION,
    '2': obd.commands.ELM_VOLTAGE,
}

dtc_info = {
    '0': None,
    '1': obd.commands.GET_DTC,  # Codes d'erreur
    '2': obd.commands.CLEAR_DTC,
    '3': obd.commands.STATUS,
    '4' : obd.commands.GET_CURRENT_DTC
}

pid_info = {
    '0': None,
    '1' : obd.commands.PIDS_A,
    '2' : obd.commands.PIDS_B,
    '3' : obd.commands.PIDS_9A
}

engine_info = {
    '0': None,
    '1' : obd.commands.COOLANT_TEMP,
    '2' : obd.commands.SPEED,
    '3' : obd.commands.ENGINE_LOAD,
}

menu = ['Quitter', 'ELM327 informations', 'Gestion des erreurs','Moteur infos','PID infos']



def display_menu():
    print(COLOR_BLUE + "╔═════════════════════════════════════════════════════════════════════╗" + COLOR_RESET)
    print(COLOR_BLUE + "║                       OBD2: MENU PRINCIPAL                          ║" + COLOR_RESET)
    print(COLOR_BLUE + "╠═════════════════════════════════════════════════════════════════════╣" + COLOR_RESET)
    
    for i, item in enumerate(menu):
        print(f"{COLOR_BLUE}║ {i}: {item} {' ' * (40 - len(item))}                        ║{COLOR_RESET}")
    
    print(COLOR_BLUE + "╚═════════════════════════════════════════════════════════════════════╝" + COLOR_RESET)

def get_user_choice(max_choice):
    while True:
        try:
            choice = int(input(COLOR_BLUE+"\nChoix du menu : "+COLOR_RESET))
            if 0 <= choice < max_choice:
                return choice
            else:
                print(COLOR_RED + "Choix invalide. Veuillez réessayer." + COLOR_RESET)
        except ValueError:
            print(COLOR_RED + "Veuillez entrer un nombre valide." + COLOR_RESET)

def execute_command(command_dict):

    print(COLOR_GREEN + "\n╔═════════════════════════════════════════════════════════════════════╗" + COLOR_RESET)
    print(COLOR_GREEN + "║                       Commandes Disponibles                         ║" + COLOR_RESET)
    print(COLOR_GREEN + "╠═════════════════════════════════════════════════════════════════════╣" + COLOR_RESET)

    for key, value in command_dict.items():
        command_name = value.name if value else 'MAIN_MENU'
        print(f"{COLOR_GREEN}║{key}: {command_name:<30}                                    ║{COLOR_RESET}")

    print(COLOR_GREEN + "╚═════════════════════════════════════════════════════════════════════╝" + COLOR_RESET)

    cmd_choice = input(COLOR_GREEN+"\nChoix de la commande : "+COLOR_RESET)
    print()
    
    # Vérifiez si l'utilisateur a choisi '0' pour retourner au menu principal
    if cmd_choice == '0':
        return  # Retourne au menu principal sans exécuter de commande

    cmd = command_dict.get(cmd_choice)

    if cmd is not None:

        if DEVELOPER_MODE == False : response = connection.query(cmd)

        if DEVELOPER_MODE == False and response.value is not None:
            if cmd == obd.commands.GET_DTC:
                if(response.value):
                    for code, description in response.value:
                        print(f"{COLOR_BLUE}{code} : {description}{COLOR_RESET}")
                else: print(COLOR_GREEN+"Aucune erreur detectée"+COLOR_RESET)
            elif cmd == obd.commands.STATUS:
                print(f"{COLOR_BLUE}Nombre d'erreur depuis dernier clear: {response.value.DTC_count}{COLOR_RESET}")
                print(f"{COLOR_BLUE}Moteur allumé: {response.value.MIL}{COLOR_RESET}")
                print(f"{COLOR_BLUE}Type d'allumage: {response.value.ignition_type}{COLOR_RESET}")
            else:
                print(f"{COLOR_BLUE}{cmd.name}: {response.value}{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}{cmd.name}: Pas de données disponibles.{COLOR_RESET}\n")
    else:
        print(COLOR_RED + "Commande invalide." + COLOR_RESET)
    
    time.sleep(2)

def main():
    
    try:
        if DEVELOPER_MODE == False:
        # Vérification de la connexion
            if connection.is_connected():
                print(COLOR_GREEN + "Connecté à l'OBD-II avec succès." + COLOR_RESET)
                protocol = connection.protocol_id()
                print(f'Le protocole utilisé est: {obd_protocols.get(protocol, "Inconnu")}')
            else:
                print(COLOR_RED + "Échec de la connexion à l'OBD-II." + COLOR_RESET)
                return

        # Menu interactif
        while True:
            display_menu()
            choice = get_user_choice(len(menu))

            if choice == 0:
                print(COLOR_YELLOW + "Fermeture de la connexion et sortie." + COLOR_RESET)
                break  # Quitter la boucle
            
            elif choice == 1:
                execute_command(elm_info)
            
            elif choice == 2:
                execute_command(dtc_info)
            
            elif choice == 3:
                execute_command(engine_info)

            elif choice == 4:
                execute_command(pid_info)

    except Exception as e:
        print(f"{COLOR_RED}Une erreur s'est produite : {e}{COLOR_RESET}")
    finally:
        # Fermer la connexion
        if DEVELOPER_MODE == False : connection.close()
        print(COLOR_GREEN + "Connexion OBD-II fermée." + COLOR_RESET)

if __name__ == "__main__":
    main()
