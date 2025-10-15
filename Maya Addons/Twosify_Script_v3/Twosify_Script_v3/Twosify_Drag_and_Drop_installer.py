import os
import shutil
import maya.cmds as cmds
import maya.mel as mel

def create_shelf_from_script():
    # Path to this file
    this_dir = os.path.dirname(__file__)
    script_name = "twosify_script.py"
    script_path = os.path.join(this_dir, script_name)
    
    # Icon detection and copying
    icon_name = "twosify_icon.png"
    source_icons_folder = os.path.join(this_dir, "icons")
    source_icon_path = os.path.join(source_icons_folder, icon_name)
    
    # Get Maya's user preferences directory and create icons path
    maya_prefs_dir = cmds.internalVar(userPrefDir=True)
    maya_icons_dir = os.path.join(maya_prefs_dir, 'icons')
    target_icon_path = os.path.join(maya_icons_dir, icon_name)
    
    # Debug info
    print("=== DEBUG INFO ===")
    print(f"Maya prefs directory: {maya_prefs_dir}")
    print(f"Source icon path: {source_icon_path}")
    print(f"Target icons directory: {maya_icons_dir}")
    print(f"Target icon path: {target_icon_path}")
    print(f"Source icon exists: {os.path.exists(source_icon_path)}")
    print(f"Target directory exists: {os.path.exists(maya_icons_dir)}")
    
    # Default icon if custom icon not found
    default_icon = "commandButton.png"
    shelf_icon = default_icon
    
    # Copy custom icon if exists
    if os.path.exists(source_icon_path):
        try:
            if not os.path.exists(maya_icons_dir):
                os.makedirs(maya_icons_dir)
                print(f"Created Maya icons directory: {maya_icons_dir}")
            
            shutil.copy(source_icon_path, target_icon_path)
            print(f"Copied icon to {target_icon_path}")
            
            if os.path.exists(target_icon_path):
                shelf_icon = target_icon_path
            else:
                shelf_icon = default_icon
        except Exception as e:
            print(f"Failed to copy icon: {e}")
            shelf_icon = default_icon
    else:
        print(f"Custom icon not found, using default: {default_icon}")

    if not os.path.exists(script_path):
        cmds.warning(f"Could not find {script_name} next to DragAndDrop.py")
        return

    # Read the script content
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()

    # Get current shelf
    shelf = mel.eval('$gShelfTopLevel=$gShelfTopLevel')
    current_shelf = cmds.tabLayout(shelf, q=True, st=True)

    try:
        # --- Remove old Twosify button if it exists ---
        existing_buttons = cmds.shelfLayout(current_shelf, q=True, ca=True) or []
        for btn in existing_buttons:
            if cmds.shelfButton(btn, q=True, label=True) == "Twosify":
                cmds.deleteUI(btn)
    except Exception as e:
        pass

    # Create new shelf button
    cmds.shelfButton(
        label="Twosify",
        parent=current_shelf,
        annotation="Run Twosify Script",
        image=shelf_icon,
        command=script_content,
        sourceType="python"
    )

    # Success message
    cmds.inViewMessage(
        amg='<span style="color: yellow; font-size:14pt;">Twosify</span> installed to Shelf.', 
        pos='midCenter', 
        fade=True
    )
    print("=== END DEBUG INFO ===")


create_shelf_from_script()

    
