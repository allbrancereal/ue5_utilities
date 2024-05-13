import os
import json

def create_plugin_files(plugin_name, module_name, module_type, loading_phase):
    # Create the plugin directory
    os.makedirs(plugin_name, exist_ok=True)

    # Create or update the .uplugin file
    uplugin_path = os.path.join(plugin_name, plugin_name + '.uplugin')
    if os.path.exists(uplugin_path):
        with open(uplugin_path, 'r') as f:
            uplugin_data = json.load(f)
        uplugin_data['Modules'].append({
            "Name": module_name,
            "Type": module_type,
            "LoadingPhase": loading_phase
        })
    else:
        uplugin_data = {
            "FileVersion": 3,
            "FriendlyName": plugin_name,
            "Version": 1,
            "VersionName": "1.0",
            "CreatedBy": "Your Name",
            "Description": "Description of " + plugin_name,
            "Category": "Category",
            "Modules": [
                {
                    "Name": module_name,
                    "Type": module_type,
                    "LoadingPhase": loading_phase
                }
            ]
        }
    with open(uplugin_path, 'w') as f:
        json.dump(uplugin_data, f, indent=4)

    # Create the module directory
    module_dir = os.path.join(plugin_name, 'Source', module_name)
    os.makedirs(os.path.join(module_dir, 'Public'), exist_ok=True)
    os.makedirs(os.path.join(module_dir, 'Private'), exist_ok=True)

    # Create the .h and .cpp files for the module
    with open(os.path.join(module_dir, 'Public', module_name + '.h'), 'w') as f:
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

    with open(os.path.join(module_dir, 'Private', module_name + '.cpp'), 'w') as f:
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

    # Create the Build.cs file for the module
    with open(os.path.join(module_dir, module_name + '.Build.cs'), 'w') as f:
        f.write(f"""
using UnrealBuildTool;

public class {module_name} : ModuleRules
{{
    public {module_name}(ReadOnlyTargetRules Target) : base(Target)
    {{
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
    
        PublicDependencyModuleNames.AddRange(new string[] {{ "Core", "CoreUObject", "Engine", "InputCore" }});
    
        PrivateDependencyModuleNames.AddRange(new string[] {{  }});
    }}
}}
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
            module_type = input("Enter the type of the module (e.g., 'Runtime'): ")
            loading_phase = input("Enter the loading phase of the module (e.g., 'Default'): ")
            create_plugin_files(plugin_name, module_name, module_type, loading_phase)
        elif choice == '2':
            plugin_name = input("Enter the name of the plugin: ")
            module_name = input("Enter the name of the new module: ")
            module_type = input("Enter the type of the module (e.g., 'Runtime'): ")
            loading_phase = input("Enter the loading phase of the module (e.g., 'Default'): ")
            create_plugin_files(plugin_name, module_name, module_type, loading_phase)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
