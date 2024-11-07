import yaml
import argparse
import subprocess
import os
from phoebusgen import screen, widget

def main_opigen():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate a Phoebus launcher.bob with tabs from a YAML configuration.")
    parser.add_argument(
        "--yaml",
        type=str,
        required=True,
        help="Path to the YAML configuration file."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="launcher.bob",
        help="Output path for the generated launcher.bob file (default: launcher.bob)"
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Phoebus Launcher",
        help="Title for the launcher (default: Phoebus Launcher)"
    )
    parser.add_argument(
        "--clone-dir",
        type=str,
        default="common",
        help="Directory to clone the OPI URL into (default: common)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1900,
        help="Width of the launcher screen (default: 1900)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1400,
        help="Height of the launcher screen (default: 1400)"
    )
    args = parser.parse_args()

    # Load YAML configuration
    with open(args.yaml, 'r') as f:
        config = yaml.safe_load(f)

    # Clone each unique OPI URL if it hasn’t been cloned already
    cloned_urls = set()
    for device in config:
        opi_section = device.get('opi', {})
        opi_url = opi_section.get('url')
        
        if opi_url and opi_url not in cloned_urls:
            clone_path = os.path.join(args.clone_dir, os.path.basename(opi_url))
            if not os.path.exists(clone_path):
                print(f"Cloning {opi_url} into {clone_path}")
                subprocess.run(["git", "clone", opi_url, clone_path])
            else:
                print(f"Repository {opi_url} already cloned in {clone_path}.")
            cloned_urls.add(opi_url)

    # Group devices by 'devgroup'
    devgroups = {}
    for device in config:
        devgroup = device.get('devgroup')
        if devgroup not in devgroups:
            devgroups[devgroup] = []
        devgroups[devgroup].append(device)

    # Create Phoebus screen with specified dimensions and NavigationTabs for tab layout
    launcher_screen = screen(title=args.title, width=args.width, height=args.height)
    nav_tabs = widget.NavigationTabs()

    # Loop over each devgroup and create a tab for it
    for devgroup, devices in devgroups.items():
        # Create a tab for each devgroup
        devgroup_tab = widget.Tab(title=devgroup)
        
        for device in devices:
            # Extract opi section and macros
            opi_section = device.get('opi', {})
            main_bob = opi_section.get('main')
            macros = opi_section.get('macro', [])
            macro_values = {macro['name']: macro['value'] for macro in macros}
            
            # Set the action path to the cloned directory
            action_path = os.path.join(args.clone_dir, os.path.basename(opi_url), main_bob)

            # Add an action button to call the .bob file with macros in each tab
            devgroup_tab.add_widget(
                widget.ActionButton(
                    label=f"Launch {device['name']}",
                    action=action_path,
                    macros=macro_values
                )
            )

        # Add the devgroup tab to NavigationTabs
        nav_tabs.add_tab(devgroup_tab)

    # Add NavigationTabs to the screen and save
    launcher_screen.add_widget(nav_tabs)
    launcher_screen.save(args.output)
    print(f"Generated Phoebus launcher with tabs at {args.output} titled '{args.title}'")

if __name__ == "__main__":
    main_opigen()
