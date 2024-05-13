import os
import json
import glob
import tkinter as tk
from tkinter import filedialog


root = tk.Tk()
root.withdraw()

UE_PROJECT_PATH = filedialog.askdirectory()
# Find the uproject file
uproject_file = filedialog.askopenfilename()

# Template for the UObject class header file
UOBJECT_H_TEMPLATE = '''\n
#pragma once

#include "CoreMinimal.h"
#include "{module_name}Object.generated.h"

UCLASS()
class {module_name}Object : public UObject
{{
    GENERATED_BODY()

public:
    void Initialize(); // Declare Initialize method

    // Add your class properties and methods here
}};
'''

# Template for the UObject class source file
UOBJECT_CPP_TEMPLATE = '''\n
#include "{module_name}Object.h"

void {module_name}Object::Initialize()
{{
    // Add your custom initialization code here
}}
'''

# Template for the .cpp file
CPP_TEMPLATE = '''\n
#include "{module_name}.h"

void {module_name}Module::StartupModule()
{{
    // This code will execute after your module is loaded into memory (but after global variables are initialized, of course.)
}}

void {module_name}Module::ShutdownModule()
{{
    // This function may be called during shutdown to clean up your module. For modules that support dynamic reloading,
    // we call this function before unloading the module.
}}

IMPLEMENT_PRIMARY_GAME_MODULE( {module_name}Module, {module_name}, "{module_name}" );
'''

# Template for the .h file
H_TEMPLATE = '''\n
#pragma once

#include "Modules/ModuleManager.h"

class {module_name}Module : public IModuleInterface
{{
public:

    /** IModuleInterface implementation */
    void StartupModule() override;
    void ShutdownModule() override;
}};
'''

BUILD_CS_TEMPLATE = '''\
using UnrealBuildTool;

public class {module_name}Module : ModuleRules
{{
    public {module_name}Module(ReadOnlyTargetRules Target) : base(Target)
    {{
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[] {{ "Core", "CoreUObject", "Engine", "InputCore" }});

        PrivateDependencyModuleNames.AddRange(new string[] {{  }});

        PrivateIncludePaths.AddRange(new string[] {{ "{module_name}Module/Private" }});
        // Uncomment if you are using Slate UI
        // PrivateDependencyModuleNames.AddRange(new string[] {{ "Slate", "SlateCore" }});

        // Uncomment if you are using online features
        // PrivateDependencyModuleNames.Add("OnlineSubsystem");

        // To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
    }}
}};
'''


def create_module(module_name, module_type, loading_phase):
    # Create new module directories
    os.makedirs(os.path.join(UE_PROJECT_PATH, "Source", module_name, "Public"))
    os.makedirs(os.path.join(UE_PROJECT_PATH, "Source", module_name, "Private"))

    # Create .cpp and .h files
    with open(os.path.join(UE_PROJECT_PATH, "Source", module_name, "Public", f"{module_name}Module.h"), "w") as f:
        f.write(H_TEMPLATE.format(module_name=module_name))
    with open(os.path.join(UE_PROJECT_PATH, "Source", module_name, "Private", f"{module_name}Module.cpp"), "w") as f:
        f.write(CPP_TEMPLATE.format(module_name=module_name))

    # Create UObject class files
    with open(os.path.join(UE_PROJECT_PATH, "Source", module_name, "Public", f"{module_name}Object.h"), "w") as f:
        f.write(UOBJECT_H_TEMPLATE.format(module_name=module_name))
    with open(os.path.join(UE_PROJECT_PATH, "Source", module_name, "Private", f"{module_name}Object.cpp"), "w") as f:
        f.write(UOBJECT_CPP_TEMPLATE.format(module_name=module_name))

    # Create .Build.cs file
    with open(os.path.join(UE_PROJECT_PATH, "Source", module_name, f"{module_name}.Build.cs"), "w") as f:
        f.write(BUILD_CS_TEMPLATE.format(module_name=module_name))

    # Update uproject file
    with open(uproject_file, "r+") as f:
        uproject_data = json.load(f)
        uproject_data["Modules"].append({"Name": module_name, "Type": module_type, "LoadingPhase": loading_phase})
        f.seek(0)
        f.truncate()
        json.dump(uproject_data, f, indent=4)


def main():
    while True:
        print("Please run this from the same folder as your .uproject file")
        print("1. Create new module")
        print("2. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            module_name = input("Enter the name of the new module: ")
            module_type = input("Enter the type of the new module: ")
            loading_phase = input("Enter the loading phase of the new module: ")
            create_module(module_name, module_type, loading_phase)
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please enter 1, 2")

if __name__ == "__main__":
    main()
