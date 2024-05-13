import os

def create_plugin_files(plugin_name, module_name):
    # Create the plugin directory
    os.makedirs(plugin_name, exist_ok=True)

    # Create the .uplugin file
    with open(os.path.join(plugin_name, plugin_name + '.uplugin'), 'w') as f:
        f.write(f"""
{{
    "FileVersion": 3,
    "FriendlyName": "{plugin_name}",
    "Version": 1,
    "VersionName": "1.0",
    "CreatedBy": "Your Name",
    "Description": "Description of {plugin_name}",
    "Category": "Category",
    "Modules": [
        {{
            "Name": "{module_name}",
            "Type": "Runtime",
            "LoadingPhase": "Default"
        }}
    ]
}}
        """)

    # Create the module directory
    os.makedirs(os.path.join(plugin_name, 'Source', module_name), exist_ok=True)

    # Create the .h and .cpp files for the module
    with open(os.path.join(plugin_name, 'Source', module_name, module_name + '.h'), 'w') as f:
        f.write(f"""
#pragma once

#include "Modules/ModuleManager.h"

class F{module_name}Module : public IModuleInterface
{{
public:
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;
}};
        """)

    with open(os.path.join(plugin_name, 'Source', module_name, module_name + '.cpp'), 'w') as f:
        f.write(f"""
#include "{module_name}.h"

void F{module_name}Module::StartupModule()
{{
    // This code will execute after your module is loaded into memory
}}

void F{module_name}Module::ShutdownModule()
{{
    // This function may be called during shutdown to clean up your module
}}

IMPLEMENT_MODULE(F{module_name}Module, {module_name})
        """)

def main():
    while True:
        print("1. Create a new plugin")
        print("2. Add a module to an existing plugin")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            plugin_name = input("Enter the name of the new plugin: ")
            module_name = input("Enter the name of the first module: ")
            create_plugin_files(plugin_name, module_name)
        elif choice == '2':
            plugin_name = input("Enter the name of the plugin: ")
            module_name = input("Enter the name of the new module: ")
            create_plugin_files(plugin_name, module_name)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
