## Created by Ehsan Bayat, 2025
# Convert animation on twos, threes or however you like and attach it to a camera without losing your animation data.
# Convert you spline animation to stepped without losing any of your splines and keys.
# v003


import maya.cmds as cmds
import maya.mel as mel
import json
import os



def set_outliner_color(obj, color=(0.75, 0.5, 0.9)):

    if not cmds.objExists(obj):
        cmds.warning(f"Object {obj} does not exist.")
        return
    
    try:
        cmds.setAttr(f"{obj}.useOutlinerColor", 1)
        cmds.setAttr(f"{obj}.outlinerColor", color[0], color[1], color[2], type="double3")
        print(f"Outliner color for {obj} set to {color}")
    except Exception as e:
        cmds.warning(f"Failed to set outliner color: {e}")



def get_frames_on_ones():
    """
    Returns a list of frames in 1s (every frame in timeline range).
    """
    min_time = int(cmds.playbackOptions(q=True, min=True))
    max_time = int(cmds.playbackOptions(q=True, max=True))
    return list(range(min_time, max_time + 1))



def set_keys_ones_anim_layer():
    
    
    sel = cmds.ls(sl=True)
    min_time = int(cmds.playbackOptions(q=True, min=True))
    max_time = int(cmds.playbackOptions(q=True, max=True))
    
    frames_list = get_frames_on_ones()

    cmds.waitCursor(state=True)  
     
    try:
        cmds.setKeyframe(t = (min_time))
    except:
        return
                
        
    if sel:    
        cmds.setKeyframe(i=True, t=(frames_list))
    cmds.waitCursor(state=False)
        



def get_frames_every_three():
    """
    Returns a list of frames at every 3 frames
    (e.g. 1, 4, 7, 10, ...), based on the playback range.
    """
    min_time = int(cmds.playbackOptions(q=True, min=True))
    max_time = int(cmds.playbackOptions(q=True, max=True))

    return list(range(min_time, max_time + 1, 3))



def set_keys_threes_anim_layer():
    
    
    sel = cmds.ls(sl=True)
    min_time = int(cmds.playbackOptions(q=True, min=True))
    max_time = int(cmds.playbackOptions(q=True, max=True))
    
    frames_list = get_frames_every_three()


    keys = cmds.keyframe(sel , q=True) or []  
    cmds.waitCursor(state=True)  
    if keys:    
        cmds.cutKey(t = (min_time, max_time))
        
    try:
        cmds.setKeyframe(t = (min_time))
    except:
        return
                
        
    if sel:    
        cmds.setKeyframe(i=True, t=(frames_list))
    cmds.waitCursor(state=False)
        


def generate_twos_threes_pattern():
    """
    Returns a list of frames in a 2,3,2,3... alternating pattern
    based on the current Maya timeline playback range.
    """
    min_time = int(cmds.playbackOptions(q=True, min=True))
    max_time = int(cmds.playbackOptions(q=True, max=True))

    pattern = [2, 3]  # alternating step sizes
    step_index = 0

    frames = []
    time = min_time
    while time <= max_time:
        frames.append(time)
        time += pattern[step_index % len(pattern)]
        step_index += 1

    return frames




def set_keys_twos_threes_anim_layer():
    
    
    sel = cmds.ls(sl=True)
    min_time = int(cmds.playbackOptions(q=True, min=True))
    max_time = int(cmds.playbackOptions(q=True, max=True))
    
    frames_list = generate_twos_threes_pattern()


    keys = cmds.keyframe(sel , q=True) or []  
    cmds.waitCursor(state=True)  
    if keys:    
        cmds.cutKey(t = (min_time, max_time))
        
    try:
        cmds.setKeyframe(t = (min_time))
    except:
        return
                
        
    if sel:    
        cmds.setKeyframe(i=True, t=(frames_list))
    cmds.waitCursor(state=False)
        


def get_frames_three_four():
    """
    Returns a list of frames in a 3–4 alternating pattern
    (e.g. 1, 4, 8, 11, 15, ...), based on the playback range.
    """
    min_time = int(cmds.playbackOptions(q=True, min=True))
    max_time = int(cmds.playbackOptions(q=True, max=True))

    pattern = [3, 4]  # alternating steps
    step_index = 0
    frames = []

    time = min_time
    while time <= max_time:
        frames.append(time)
        time += pattern[step_index % len(pattern)]
        step_index += 1

    return frames



def set_keys_threes_fours_anim_layer():
    
    
    sel = cmds.ls(sl=True)
    min_time = int(cmds.playbackOptions(q=True, min=True))
    max_time = int(cmds.playbackOptions(q=True, max=True))
    
    frames_list = get_frames_three_four()


    keys = cmds.keyframe(sel , q=True) or []  
    cmds.waitCursor(state=True)  
    if keys:    
        cmds.cutKey(t = (min_time, max_time))
        
    try:
        cmds.setKeyframe(t = (min_time))
    except:
        return
                
        
    if sel:    
        cmds.setKeyframe(i=True, t=(frames_list))
    cmds.waitCursor(state=False)
        
        
  


def set_keys_twos_anim_layer():
    
    
    sel = cmds.ls(sl=True)
    min_time = int(cmds.playbackOptions(q=True, min=True))
    max_time = int(cmds.playbackOptions(q=True, max=True))
    
    timelineRange = range(min_time, max_time+1)
    
    odd_frames=[]
    even_frames=[]
    for time in timelineRange:
        remainder = time % 2
        if remainder > 0:
            odd_frames.append(time)
        else:
            even_frames.append(time)

    keys = cmds.keyframe(sel , q=True) or []  
    cmds.waitCursor(state=True)  
    if keys:    
        cmds.cutKey(t = (min_time, max_time))
        
    try:
        cmds.setKeyframe(t = (min_time))
    except:
        return
                
        
    if sel:    
        if (min_time % 2 == 0):        
            cmds.setKeyframe(i=True, t=(even_frames))
        else:        
            cmds.setKeyframe(i=True, t=(odd_frames))
        cmds.waitCursor(state=False)
                
                
                
# Class variable to store copied key times (for backwards compatibility)
copied_key_times = []

def paste_action(mode="Pose to Pose"):
    """
    Standalone paste action function extracted from PoseToPoseNative class
    
    Args:
        mode (str): Either "Pose to Pose" or "Channels" to determine paste behavior
    """
    print(f"Paste pressed - current option: {mode}")
    
    if mode == "Pose to Pose":
        clean_range_script()
    elif mode == "Channels":
        paste_key_times_smart()

def clean_range_script():
    """
    Paste script - loads key times from JSON file and applies them to selected objects
    Works exactly like the "dada" logic
    """
    try:
        cmds.undoInfo(openChunk=True)
        
        # Load key times from JSON file
        desktop_path = get_desktop_path()
        json_filename = "esn_key_times.json"
        json_path = os.path.join(desktop_path, json_filename)
        
        if not os.path.exists(json_path):
            # Fallback to class variable if JSON doesn't exist
            allKeys = copied_key_times[:]
            if not allKeys:
                cmds.warning("No key times found. Please use Copy button first.")
                print("No esn_key_times.json file found and no key times copied. Please use Copy button first.")
                return
            print("Using fallback key times from memory.")
        else:
            # Load from JSON file
            try:
                with open(json_path, "r") as f:
                    json_data = json.load(f)
                
                allKeys = json_data.get("key_times", [])
                
                if not allKeys:
                    cmds.warning("No key times found in JSON file. Please use Copy button first.")
                    print("No key times found in JSON file.")
                    return
                    
                print(f"Loaded key times from JSON: {allKeys}")
                print(f"JSON loaded from: {json_path}")
                
            except Exception as e:
                cmds.warning("Error reading JSON file. Using fallback if available.")
                print(f"Error reading esn_key_times.json: {str(e)}")
                allKeys = copied_key_times[:]
                if not allKeys:
                    cmds.warning("No fallback key times available.")
                    return
                print("Using fallback key times from memory.")
        
        # Check if anything is selected (same as dada logic)
        sel = cmds.ls(sl=True)
        if len(sel) == 0:
            print("No objects selected. Please select objects to paste keys.")
            return

        # Store current time (same as dada logic)
        CT = cmds.currentTime(q=1)

        # Get the stored playback range from JSON (not current range)
        stored_range = json_data.get("playback_range", [int(cmds.playbackOptions(q=True, min=True)), int(cmds.playbackOptions(q=True, max=True))])
        Minn = stored_range[0]
        Maxx = stored_range[1]
        print(f"Using stored playback range: {Minn} to {Maxx}")

        objects = cmds.ls(sl=1)

        cmds.waitCursor(state=True)
        
        # Find objects with no keys and add a key at the first copied time (same as dada logic)
        objWithNoKeys = []
        for obj in objects:
            keyframes = cmds.keyframe(obj, q=1)
            if keyframes is None:
                objWithNoKeys.append(obj)

        # Set keyframes on objects that don't have any at the first copied key time (same as dada logic)
        if objWithNoKeys and allKeys:
            for obj in objWithNoKeys:
                cmds.setKeyframe(obj, t=allKeys[0])

        # Get all frames in the playback range (same as dada logic)
        allFrames = range(Minn, Maxx+1)

        # Set keyframes at all copied key times with INSERT flag (same as dada logic)
        for key in allKeys:
            cmds.setKeyframe(objects, i=True, t=key)

        # Remove keyframes that are NOT in our copied keys list (same as dada logic)
        for frame in allFrames:    
            if frame not in allKeys:
                cmds.cutKey(objects, t=(frame, frame))

        # Restore current time (same as dada logic)
        cmds.currentTime(CT)
        cmds.waitCursor(state=False)
        
        print(f"Applied key timing exactly like dada logic: {allKeys}")
        print("Paste completed.")
        
    except Exception as e:
        cmds.waitCursor(state=False)
        print(f"Error in paste script: {str(e)}")
    finally:
        cmds.undoInfo(closeChunk=True)

def paste_key_times_smart():
    """
    Smart Paste Key Times - syncs keyframes based on JSON data
    Uses object-specific timing with fallback to reference object
    """
    try:
        # Load JSON file from Desktop
        desktop_path = get_desktop_path()
        json_filename = "maya_key_timing.json"
        json_path = os.path.join(desktop_path, json_filename)
        
        if not os.path.exists(json_path):
            cmds.warning("JSON file not found. Please use Smart Copy first.")
            print("JSON file not found. Please use Smart Copy first.")
            return

        with open(json_path, "r") as f:
            data = json.load(f)

        if not data:
            cmds.warning("JSON is empty or invalid.")
            print("JSON is empty or invalid.")
            return

        selected = cmds.ls(sl=True)
        if not selected:
            cmds.warning("Please select at least one object.")
            print("Please select at least one object.")
            return

        time_start = cmds.playbackOptions(q=True, min=True)
        time_end = cmds.playbackOptions(q=True, max=True)
        timeline_min = float(time_start)
        timeline_max = float(time_end)

        # Reference object for fallback
        ref_obj = next(iter(data))

        for obj in selected:
            # Use object's own key timing if exists, else fallback to ref_obj
            obj_key_data = data.get(obj, data[ref_obj])

            for attr, ref_times in obj_key_data.items():
                full_attr = f"{obj}.{attr}"
                if not cmds.objExists(full_attr):
                    continue

                # Filter keys strictly within timeline range
                filtered_ref_times = [t for t in ref_times if timeline_min <= t <= timeline_max]
                ref_set = set(filtered_ref_times)

                actual_times = cmds.keyframe(full_attr, q=True, timeChange=True)
                actual_set = set(actual_times) if actual_times else set()

                # Keys to add (insert)
                to_add = [t for t in sorted(ref_set - actual_set) if timeline_min <= t <= timeline_max]
                # Keys to remove (cut)
                to_remove = [t for t in sorted(actual_set - ref_set) if timeline_min <= t <= timeline_max]

                for t in to_add:
                    cmds.setKeyframe(full_attr, time=t, insert=True)
                for t in to_remove:
                    cmds.cutKey(full_attr, time=(t, t), option="keys")

                if to_add or to_remove:
                    print(f"Synced {full_attr}: +{len(to_add)} keys, -{len(to_remove)} keys inside timeline")

        print("Smart paste completed. Keyframe sync with object-specific timing complete.")
        
    except Exception as e:
        print(f"Error in smart paste: {str(e)}")


def show_feedback_message(message):
    """Show feedback message using Maya's inViewMessage"""
    try:
        cmds.inViewMessage(
            amg=message,
            pos='botCenter',
            fade=True,
            fadeStayTime=1500,
            fadeOutTime=500
        )
    except Exception as e:
        # Fallback to print if inViewMessage fails
        print(f"Feedback: {message}")

def get_selected_channelbox_attrs():
    """Get selected attributes from the channel box"""
    try:
        channel_box = mel.eval('$tmp=$gChannelBoxName')

        main_selected = cmds.channelBox(channel_box, q=True, selectedMainAttributes=True) or []
        shape_selected = cmds.channelBox(channel_box, q=True, selectedShapeAttributes=True) or []
        output_selected = cmds.channelBox(channel_box, q=True, selectedOutputAttributes=True) or []
        history_selected = cmds.channelBox(channel_box, q=True, selectedHistoryAttributes=True) or []

        return list(set(main_selected + shape_selected + output_selected + history_selected))
    except:
        return []

def get_all_keyable_attrs(obj):
    """Get all keyable, visible, user-editable attributes on the object."""
    try:
        all_attrs = cmds.listAttr(obj, keyable=True, visible=True, unlocked=True) or []
        return all_attrs
    except:
        return []




def copy_action(mode="Pose to Pose"):
    """
    Standalone copy action function extracted from PoseToPoseNative class
    
    Args:
        mode (str): Either "Pose to Pose" or "Channels" to determine copy behavior
    """
    print(f"Copy pressed - current option: {mode}")
    
    if mode == "Pose to Pose":
        copy_key_times_script()
    elif mode == "Channels":
        copy_key_times_smart()

def copy_key_times_script():
    """
    Copy Key Times script - stores keyframe timing from selected objects to JSON file
    Even handles objects with no keys by storing empty timing data
    """
    try:
        cmds.undoInfo(openChunk=True)
        
        sel = cmds.ls(sl=True)
        if len(sel) == 0:
            print("No objects selected for copy operation.")
            return
        
        # Get playback range
        Min_t = int(cmds.playbackOptions(q=True, min=True))
        Max_t = int(cmds.playbackOptions(q=True, max=True))
        
        # Get all keys in the range from selected objects
        allKeys = cmds.keyframe(sel, q=True, t=(Min_t, Max_t))
        
        # Handle case where no keys exist - store empty list
        if allKeys:
            # Remove duplicates and sort
            key_times = list(set(allKeys))
            key_times.sort()
            print(f"Found keyframes: {key_times}")
        else:
            # No keys found - store empty list but still create JSON
            key_times = []
            print("No keyframes found on selected objects. Storing empty key times data.")
        
        # Save to JSON file on Desktop
        desktop_path = get_desktop_path()
        json_filename = "esn_key_times.json"
        json_path = os.path.join(desktop_path, json_filename)
        
        # Create JSON data structure
        json_data = {
            "key_times": key_times,
            "playback_range": [Min_t, Max_t],
            "source_objects": sel,
            "has_keys": len(key_times) > 0
        }
        
        with open(json_path, "w") as f:
            json.dump(json_data, f, indent=4)
        
        # Show feedback
        show_feedback_message("Copied Key Time")
        if key_times:
            print(f"Copied key times to JSON: {key_times}")
        else:
            print("Copied empty key times data to JSON (no keys found)")
        print(f"JSON saved to: {json_path}")
                
    except Exception as e:
        print(f"Error in copy_key_times_script: {str(e)}")
    finally:
        cmds.undoInfo(closeChunk=True)

def copy_key_times_smart():
    """
    Smart Copy Key Times - works with channel box selections
    Saves key timing data to JSON file on Desktop
    """
    try:
        cmds.undoInfo(openChunk=True)
        
        selected = cmds.ls(sl=True)
        if not selected:
            cmds.warning("No objects selected.")
            print("No objects selected for smart copy.")
            return

        result = {}

        for obj in selected:
            attrs = get_selected_channelbox_attrs()
            if not attrs:
                # No selected channels, fallback to all keyable visible attrs
                attrs = get_all_keyable_attrs(obj)

            if not attrs:
                continue

            obj_data = {}
            for attr in attrs:
                full_attr = f"{obj}.{attr}"
                if cmds.objExists(full_attr):
                    key_times = cmds.keyframe(full_attr, q=True, timeChange=True)
                    if key_times:
                        obj_data[attr] = key_times

            if obj_data:
                result[obj] = obj_data

        if not result:
            cmds.warning("No keyed attributes found on selected objects.")
            print("No keyed attributes found on selected objects.")
            return

        # Save to Desktop
        desktop_path = get_desktop_path()
        json_filename = "maya_key_timing.json"
        json_path = os.path.join(desktop_path, json_filename)

        with open(json_path, "w") as f:
            json.dump(result, f, indent=4)

        print(f"Smart copy completed. Keyframe timing saved to: {json_path}")
        show_feedback_message("Copied Key Time")
        
    except Exception as e:
        print(f"Error in smart copy: {str(e)}")
    finally:
        cmds.undoInfo(closeChunk=True)

def get_selected_channelbox_attrs():
    """Get selected attributes from the channel box"""
    try:
        channel_box = mel.eval('$tmp=$gChannelBoxName')

        main_selected = cmds.channelBox(channel_box, q=True, selectedMainAttributes=True) or []
        shape_selected = cmds.channelBox(channel_box, q=True, selectedShapeAttributes=True) or []
        output_selected = cmds.channelBox(channel_box, q=True, selectedOutputAttributes=True) or []
        history_selected = cmds.channelBox(channel_box, q=True, selectedHistoryAttributes=True) or []

        return list(set(main_selected + shape_selected + output_selected + history_selected))
    except:
        return []

def get_all_keyable_attrs(obj):
    """Get all keyable, visible, user-editable attributes on the object."""
    try:
        all_attrs = cmds.listAttr(obj, keyable=True, visible=True, unlocked=True) or []
        return all_attrs
    except:
        return []

def get_desktop_path():
        docs_dir = os.path.join(os.path.expanduser("~"))

        anim_tools_folder = os.path.join(docs_dir, "animTools")
        os.makedirs(anim_tools_folder, exist_ok=True)
        return anim_tools_folder


def show_feedback_message(message):
    """Show feedback message using Maya's inViewMessage"""
    try:
        cmds.inViewMessage(
            amg=message,
            pos='botCenter',
            fade=True,
            fadeStayTime=1500,
            fadeOutTime=500
        )
    except Exception as e:
        # Fallback to print if inViewMessage fails
        print(f"Feedback: {message}")



def create_twos_layer():

    sel = cmds.ls(sl=True)

    if sel:    
        root_layer = cmds.animLayer(query=True, root=True) or []
        animLayers = cmds.treeView("AnimLayerTabanimLayerEditor", q=True, selectItem=True) or []
        cmds.waitCursor(state=True)
        animLayerName = cmds.animLayer("TWOS", selected=True)
        # Deselect the previous selected layers
        for layer in animLayers:
            mel.eval('animLayerEditorOnSelect {0} 0;'.format(layer))    

        attrs = cmds.listAnimatable()

        for attr in attrs:
            cmds.animLayer(animLayerName, e=True, attribute = attr)
        cmds.waitCursor(state=False)
        
    else:
        cmds.confirmDialog(title="Error", message="Please select something to create an animLayer.")


def add_selected_to_anim_layer():

    sel = cmds.ls(sl=True)


    if sel:
        try:      
            animLayerName = cmds.treeView("AnimLayerTabanimLayerEditor", q=True, selectItem=True)[0]
            attrs = cmds.listAnimatable()

            for attr in attrs:
                cmds.animLayer(animLayerName, e=True, attribute = attr)
        except:
            pass


def convert_to_twos():

    animLayerName = cmds.treeView("AnimLayerTabanimLayerEditor", q=True, selectItem=True) or []
    if animLayerName:
        animLayerName = animLayerName[0]
    else:
        return
    rootLayer = cmds.animLayer(q=True, root=True)
    animLayers = cmds.treeView("AnimLayerTabanimLayerEditor", q=True, selectItem=True) or []
    min_time = cmds.playbackOptions(q=True, min=True)
    max_time = cmds.playbackOptions(q=True, max=True)
    sel = cmds.ls(sl=True)

    try:
        cmds.selectKey(cl=True)
    except:
        pass

    if sel:

        # Get the timerange selected
        playBackSlider = mel.eval('$animBot_playBackSliderPython=$gPlayBackSlider')
        timeRange = cmds.timeControl(playBackSlider, query=True, rangeArray=True)
        StartRange = timeRange[0]
        EndRange = timeRange[1] - 1
        StartRange = int(StartRange)
        EndRange = int(EndRange)
        
        
        if (EndRange - StartRange == 0):
        
            if animLayers[0] == rootLayer:
                cmds.confirmDialog(title='Error', message='Please make sure to have an animLayer selected!', button="Got it!")
                
            else:    
                cmds.animLayer(animLayerName, edit=True, override=True)  
                cmds.animLayer(animLayerName, e=True, weight=0)
                curTime = cmds.currentTime(q=True)
                keys = cmds.keyframe(q=True, t=(min_time, max_time))

                if keys:
                    cmds.waitCursor(state=True)
                    keys = list(set(keys))
                    keys.sort()
                
                    for key in keys:
                        cmds.currentTime(key)
                        cmds.setKeyframe()
                    
                    cmds.currentTime(curTime)
                    cmds.refresh(suspend=False)
                    
                    cmds.animLayer(animLayerName, e=True, weight=1)
                    cmds.keyTangent(ott="step", itt="auto")
                    
                else:
                    cmds.confirmDialog(title='Error', message='Please set some keys!', button="Got it!")
                            
        else:
        
            if animLayers[0] == rootLayer:
                cmds.confirmDialog(title='Error', message='Please make sure to have an animLayer selected!', button="Got it!")
                
            else:    
                cmds.animLayer(animLayerName, edit=True, override=True)  
                cmds.animLayer(animLayerName, e=True, weight=0)
                curTime = cmds.currentTime(q=True)
                keys = cmds.keyframe(q=True, t=(StartRange,EndRange))
                
                if keys:
                    keys = list(set(keys))
                    keys.sort()
                
                    for key in keys:
                        cmds.currentTime(key)
                        cmds.setKeyframe()
                    
                    cmds.currentTime(curTime)
                    cmds.refresh(suspend=False)
                    
                    cmds.animLayer(animLayerName, e=True, weight=1)
                    cmds.keyTangent(ott="step", itt="step")
                    
                else:
                    cmds.confirmDialog(title='Error', message='Please set some keys!', button="Got it!")
                            
        
        cmds.waitCursor(state=False)
    else:
        cmds.confirmDialog(title='Error', message='Please select something!', button="Got it!")


def simple_smart_constraint(ctrl=None, object=None, connect_to_attach_cam=False, attach_cam_object=None):
    transAttr = None
    rotAttr = None
    scaleAttr = None
    translate=True
    rotate=True
    scale=False
    maintainOffset=True 

    if translate:
        transAttr = cmds.listAttr(object, keyable=True, unlocked=True, string='translate*')     
    if rotate:
        rotAttr = cmds.listAttr(object, keyable=True, unlocked=True, string='rotate*')      
    if scale:
        scaleAttr = cmds.listAttr(object, keyable=True, unlocked=True, string='scale*')     

    rotSkip = []
    transSkip = []

    for axis in ['x','y','z']:
        if transAttr and not 'translate'+axis.upper() in transAttr:
            transSkip.append(axis)
        if rotAttr and not 'rotate'+axis.upper() in rotAttr:
            rotSkip.append(axis)

    if not transSkip:
        transSkip = 'none'
    if not rotSkip:
        rotSkip = 'none'

    constraints = []
    if rotAttr and transAttr and rotSkip == 'none' and transSkip == 'none':
        constraints.append(cmds.parentConstraint(ctrl, object, maintainOffset=maintainOffset))
    else:
        if transAttr:
            constraints.append(cmds.pointConstraint(ctrl, object, skip=transSkip, maintainOffset=maintainOffset))
        if rotAttr:
            constraints.append(cmds.orientConstraint(ctrl, object, skip=rotSkip, maintainOffset=maintainOffset))
    
    return constraints


def smart_constraint_create_attach_cam(ctrl=None, object=None):
    if not ctrl or not object:
        print("ERROR: Both ctrl and object parameters are required!")
        return
    
    # Check if objects exist
    if not cmds.objExists(ctrl):
        print(f"ERROR: Controller '{ctrl}' does not exist!")
        return
    if not cmds.objExists(object):
        print(f"ERROR: Object '{object}' does not exist!")
        return
    
    print(f"DEBUG: Both objects exist - proceeding...")
    
    transAttr = None
    rotAttr = None
    scaleAttr = None
    translate=True
    rotate=True
    scale=False
    maintainOffset=True 

    if translate:
        transAttr = cmds.listAttr(object, keyable=True, unlocked=True, string='translate*')     
    if rotate:
        rotAttr = cmds.listAttr(object, keyable=True, unlocked=True, string='rotate*')      
    if scale:
        scaleAttr = cmds.listAttr(object, keyable=True, unlocked=True, string='scale*')     

    print(f"DEBUG: transAttr = {transAttr}")
    print(f"DEBUG: rotAttr = {rotAttr}")

    rotSkip = []
    transSkip = []

    for axis in ['x','y','z']:
        if transAttr and not 'translate'+axis.upper() in transAttr:
            transSkip.append(axis)
        if rotAttr and not 'rotate'+axis.upper() in rotAttr:
            rotSkip.append(axis)

    if not transSkip:
        transSkip = 'none'
    if not rotSkip:
        rotSkip = 'none'

    print(f"DEBUG: transSkip = {transSkip}")
    print(f"DEBUG: rotSkip = {rotSkip}")

    constraints = []
    if rotAttr and transAttr and rotSkip == 'none' and transSkip == 'none':
        print("DEBUG: Creating parent constraint...")
        constraints.append(cmds.parentConstraint(ctrl, object, maintainOffset=maintainOffset))
    else:
        if transAttr:
            print("DEBUG: Creating point constraint...")
            constraints.append(cmds.pointConstraint(ctrl, object, skip=transSkip, maintainOffset=maintainOffset))
        if rotAttr:
            print("DEBUG: Creating orient constraint...")
            constraints.append(cmds.orientConstraint(ctrl, object, skip=rotSkip, maintainOffset=maintainOffset))
    
    print(f"DEBUG: Created constraints: {constraints}")
    
    # Add the Attach_Cam attribute to the object (second selection) instead of controller
    print(f"DEBUG: Checking if Attach_Cam exists on {object}...")
    
    try:
        if cmds.attributeQuery('Attach_Cam', node=object, exists=True):
            print(f"DEBUG: 'Attach_Cam' attribute already exists on {object}")
        else:
            print(f"DEBUG: Adding 'Attach_Cam' attribute to {object}...")
            cmds.addAttr(object, longName='Attach_Cam', attributeType='enum', 
                         enumName='Off:On', defaultValue=1, keyable=True)
            print(f"SUCCESS: Added 'Attach_Cam' attribute to {object}")
            
            # Verify it was added
            if cmds.attributeQuery('Attach_Cam', node=object, exists=True):
                print(f"VERIFIED: 'Attach_Cam' attribute now exists on {object}")
            else:
                print(f"ERROR: Failed to verify 'Attach_Cam' attribute on {object}")
                
    except Exception as e:
        print(f"ERROR adding attribute: {e}")
    
    # Connect the Attach_Cam attribute to control constraint weights
    for constraint in constraints:
        if constraint:  # Make sure constraint was created successfully
            print(f"DEBUG: Processing constraint {constraint}")
            
            # Handle the fact that constraints are returned in lists
            if isinstance(constraint, list):
                constraint_node = constraint[0]
            else:
                constraint_node = constraint
                
            print(f"DEBUG: Actual constraint node: {constraint_node}")
            
            # Verify the Attach_Cam attribute exists before connecting
            if cmds.attributeQuery('Attach_Cam', node=object, exists=True):
                print(f"DEBUG: Confirmed Attach_Cam exists on {object}")
                
                # Get all weight attributes of the constraint  
                weightAttrs = cmds.listAttr(constraint_node, string='*W*')
                print(f"DEBUG: Weight attributes found: {weightAttrs}")
                
                if weightAttrs:
                    for weightAttr in weightAttrs:
                        # Only connect to the actual weight attributes (skip quaternion weights)
                        if 'W0' in weightAttr or 'Weight' in weightAttr:
                            try:
                                print(f"DEBUG: Attempting to connect {object}.Attach_Cam to {constraint_node}.{weightAttr}")
                                cmds.connectAttr(f"{object}.Attach_Cam", f"{constraint_node}.{weightAttr}", force=True)
                                print(f"SUCCESS: Connected {object}.Attach_Cam to {constraint_node}.{weightAttr}")
                            except Exception as e:
                                print(f"ERROR connecting {weightAttr}: {e}")
            else:
                print(f"ERROR: Attach_Cam attribute not found on {object}")
    
    return constraints


def create_circle(master_name=None):
    # Generate unique name for the circle based on master name
    if master_name:
        base_name = f"{master_name}_esn_cam_attach"
    else:
        base_name = "Follow_Cam_esn_cam_attach"
    
    counter = 1
    circle_name = f"{base_name}_{counter:02d}"
    
    # Keep incrementing until we find a name that doesn't exist
    while cmds.objExists(circle_name):
        counter += 1
        circle_name = f"{base_name}_{counter:02d}"
    
    # Create the NURBS circle (normal in Y-axis to make it horizontal in X)
    circle = cmds.circle(normal=(0, 1, 0), name=circle_name)[0]
    circle_shape = cmds.listRelatives(circle, shapes=True)[0]
    
    # Set the color to yellow (color index 17 is yellow in Maya)
    cmds.setAttr(circle_shape + ".overrideEnabled", 1)
    cmds.setAttr(circle_shape + ".overrideColor", 17)
    
    # Lock and hide the visibility attribute
    cmds.setAttr(circle + ".visibility", lock=True)
    cmds.setAttr(circle + ".visibility", keyable=False, channelBox=False)
    
    # Make scale X, Y, Z not-keyable and hide them
    for axis in ['X', 'Y', 'Z']:
        scale_attr = circle + ".scale" + axis
        cmds.setAttr(scale_attr, keyable=False)
        cmds.setAttr(scale_attr, channelBox=False)
    
    # Turn on the display handles
    cmds.setAttr(circle + ".displayHandle", 1)

    return circle


def create_locator():
    # Generate unique name for the locator
    base_name = "Follow_Cam_Loc"
    counter = 1
    locator_name = f"{base_name}_{counter:02d}"
    
    # Keep incrementing until we find a name that doesn't exist
    while cmds.objExists(locator_name):
        counter += 1
        locator_name = f"{base_name}_{counter:02d}"
    
    # Create the locator
    locator = cmds.spaceLocator(name=locator_name)[0]
    locator_shape = cmds.listRelatives(locator, shapes=True)[0]
    
    # Set the color to red (color index 13 is red in Maya)
    cmds.setAttr(locator_shape + ".overrideEnabled", 1)
    cmds.setAttr(locator_shape + ".overrideColor", 13)
    
    # Lock and hide the visibility attribute
    cmds.setAttr(locator + ".visibility", lock=True)
    cmds.setAttr(locator + ".visibility", keyable=False, channelBox=False)
    
    # Make scale X, Y, Z not-keyable and hide them
    for axis in ['X', 'Y', 'Z']:
        scale_attr = locator + ".scale" + axis
        cmds.setAttr(scale_attr, keyable=False)
        cmds.setAttr(scale_attr, channelBox=False)
    
    # Turn on the display handles
    cmds.setAttr(locator + ".displayHandle", 1)

    return locator


def get_keys_time(objs=None):
    """
    Returns a sorted list of unique keyframe times for given objects.
    If no objects are provided, it will use the current selection.
    """
    if objs is None:
        objs = cmds.ls(selection=True)
    
    if not objs:
        return []
    
    keys_time = cmds.keyframe(objs, query=True, timeChange=True) or []
    return sorted(list(set(keys_time)))


def show_ui():
    window_name = "KeysTimeUI"
    
    # Delete existing window if it exists
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)
    
    # Create main window
    window = cmds.window(
        window_name,
        title="Twosify",
        widthHeight=(260, 230),
        sizeable=False,
        minimizeButton=False,
        maximizeButton=False,
        retain=True,
        backgroundColor=[0.12, 0.12, 0.12]
    )
    
    # Main column layout
    main_layout = cmds.columnLayout(
        adjustableColumn=True,
        columnAttach=('both', 10),
        rowSpacing=8,
        backgroundColor=[0.15, 0.15, 0.15],
        parent=window
    )
    
    # Add some spacing at the top
    cmds.separator(height=5, style='none', parent=main_layout)
    
    # Dynamic label that changes based on dropdown
    title_label = cmds.text(
        label="Stepped", 
        align='left', 
        font='boldLabelFont',
        backgroundColor=[0.15, 0.15, 0.15],
        parent=main_layout
    )
    
    # Dropdown menu
    def on_dropdown_change(selection):
        if selection == "Make It Stepped":        
            cmds.text(title_label, edit=True, label="Stepped")
            cmds.layout(make_it_twos_layout, e=True, visible=True)
            cmds.layout(attach_to_camera_layout, e=True, visible=False)
        else:
            cmds.text(title_label, edit=True, label="Camera")
            cmds.layout(make_it_twos_layout, e=True, visible=False)
            cmds.layout(attach_to_camera_layout, e=True, visible=True)
        print("Dropdown changed to:", selection)

    dropdown = cmds.optionMenu(
        label='',
        changeCommand=on_dropdown_change,
        backgroundColor=[0.23, 0.23, 0.23],
        parent=main_layout
    )
    cmds.menuItem(label="Make It Stepped")
    cmds.menuItem(label="Attach to Camera")


    # -------------------------
    # Layout for "Make It Twos"
    # -------------------------
    make_it_twos_layout = cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=6,
        backgroundColor=[0.15, 0.15, 0.15],
        parent=main_layout
    )

    cmds.separator(height=7, style='none', parent=make_it_twos_layout)

    # Primary buttons
    anim_layer_butt = cmds.button(
        label=" =  Create animLayer from Selections  = ",
        command="create_twos_layer()",
        height=28,
        backgroundColor=[0.26, 0.26, 0.26],
        parent=make_it_twos_layout
    )


    anim_layer_butt = cmds.popupMenu(parent = anim_layer_butt)
    cmds.menuItem(label='Add Selection to AnimLayer', command='add_selected_to_anim_layer()', parent=anim_layer_butt)
    cmds.menuItem(label='Set Keys On 1s', command='set_keys_ones_anim_layer()', parent=anim_layer_butt)
    cmds.menuItem(label='Set Keys On 2s', command='set_keys_twos_anim_layer()', parent=anim_layer_butt)
    cmds.menuItem(label='Set Keys On 3s', command='set_keys_threes_anim_layer()', parent=anim_layer_butt)
    cmds.menuItem(label='Set Keys On 2s-3s', command='set_keys_twos_threes_anim_layer()', parent=anim_layer_butt)
    cmds.menuItem(label='Set Keys On 3s-4s', command='set_keys_threes_fours_anim_layer()', parent=anim_layer_butt)
    
  

    # Dummy empty column to push buttons to center

    # Centered Copy/Paste buttons without stretching
    button_row = cmds.rowLayout(
        numberOfColumns=3,
        columnAttach=[(1, 'both', 0), (2, 'both', 5), (3, 'both', 0)],
        columnWidth3=(33, 80, 80),
        parent=make_it_twos_layout,
        backgroundColor=[0.15, 0.15, 0.15]
    )
    


    cmds.text(label='', parent=button_row)
    cmds.separator(height=30, style='none', parent=make_it_twos_layout)
    
    cmds.button(
        label="Copy Time",
        command='copy_action("Pose to Pose")',
        height=24,
        backgroundColor=[0.22, 0.22, 0.22],
        parent=button_row
    )
    
    cmds.button(
        label='Paste Time',
        command='paste_action("Pose to Pose")',
        height=24,
        backgroundColor=[0.22, 0.22, 0.22],
        parent=button_row
    )
    
    # Main button for this tab
    cmds.button(
        label="UPDATE LAYER",
        command="convert_to_twos()",
        height=35,
        backgroundColor=[0.35, 0.35, 0.35],
        parent=make_it_twos_layout
    )
    
    

    # -----------------------------
    # Layout for "Attach to Camera"
    # -----------------------------
    attach_to_camera_layout = cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=10,
        backgroundColor=[0.15, 0.15, 0.15],
        parent=main_layout,
        visible=False
    )
    
    # Function to assign camera from selection
    def assign_camera(*args):
        selection = cmds.ls(selection=True)
        if selection:
            # Check if selected object is a camera or camera transform
            selected_obj = selection[0]
            if cmds.nodeType(selected_obj) == 'camera':
                # It's a camera shape, get its transform
                camera_transform = cmds.listRelatives(selected_obj, parent=True)[0]
                cmds.textField(camera_field, edit=True, text=camera_transform)
                print(f"Assigned camera shape's transform: {camera_transform}")
            elif cmds.listRelatives(selected_obj, shapes=True, type='camera'):
                # It's a camera transform
                cmds.textField(camera_field, edit=True, text=selected_obj)
                print(f"Assigned camera transform: {selected_obj}")
            else:
                # Not a camera, but assign it anyway
                cmds.textField(camera_field, edit=True, text=selected_obj)
                print(f"Assigned object: {selected_obj}")
        else:
            print("No objects selected!")
    
    # Function to assign master control from selection
    def assign_master_ctrl(*args):
        selection = cmds.ls(selection=True)
        if selection:
            selected_obj = selection[0]
            cmds.textField(master_field, edit=True, text=selected_obj)
            print(f"Assigned master control: {selected_obj}")
        else:
            print("No objects selected!")
    
    # Function to get keys time from selection
    def assign_keys_time(*args):
        selection = cmds.ls(selection=True)
        if selection:
            keys_time = get_keys_time(objs=selection)
            if keys_time:
                # Convert the list of keyframe times to a string
                keys_string = ', '.join([str(int(key)) for key in keys_time])
                cmds.textField(keys_time_field, edit=True, text=keys_string)
                print(f"Found keyframe times: {keys_string}")
            else:
                cmds.textField(keys_time_field, edit=True, text="No keys found")
                print("No keyframes found on selected objects")
        else:
            print("No objects selected!")
    
    # Function to execute the main attach to camera functionality
    def attach_to_camera(*args):
        # Get values from text fields
        cam_obj = cmds.textField(camera_field, query=True, text=True)
        master_obj = cmds.textField(master_field, query=True, text=True)
        keys_time_text = cmds.textField(keys_time_field, query=True, text=True)
        
        # Validate inputs
        if not cam_obj or cam_obj.strip() == "":
            print("ERROR: No camera assigned!")
            return
        if not master_obj or master_obj.strip() == "":
            print("ERROR: No master control assigned!")
            return
        if not keys_time_text or keys_time_text.strip() == "":
            print("ERROR: No keys time assigned!")
            return

        sel = cmds.ls(sl=True)
        for s in sel:
            if cmds.objExists(s + "_esn_cam_attach_01"):
                cmds.confirmDialog(
                    title='Warning',
                    message='You have already done a setup on the selected objects. \n Please remove the old setup.',
                    button=['OK'],
                    defaultButton='OK',
                    icon='warning'
                )        
                return  


        
        # Parse the keys time string
        try:
            keys_time = [float(key.strip()) for key in keys_time_text.split(',') if key.strip()]
        except ValueError:
            print("ERROR: Invalid keys time format!")
            return

        cmds.currentTime(keys_time[0])
        
        print(f"Using camera: {cam_obj}")
        print(f"Using master: {master_obj}")
        print(f"Using keys time: {keys_time}")
        
        # Check if objects exist
        if not cmds.objExists(cam_obj):
            print(f"ERROR: Camera '{cam_obj}' does not exist!")
            return
        if not cmds.objExists(master_obj):
            print(f"ERROR: Master control '{master_obj}' does not exist!")
            return
        
        # Create follow cam group if it doesn't exist
        follow_cam_grp = "FOLLOW_CAM_GRP"
        if not cmds.objExists(follow_cam_grp):
            cmds.group(n=follow_cam_grp, empty=True)
            try:
                set_outliner_color("FOLLOW_CAM_GRP", (0.75, 0.5, 0.9)) 
            except:
                pass
        
        # Create controls
        circle_ctrl = create_circle(master_name=master_obj)
        loc_ctrl = create_locator()
        
        # Parent locator to circle, circle to group
        cmds.parent(loc_ctrl, circle_ctrl)
        cmds.parent(circle_ctrl, follow_cam_grp)
        
        # Create constraint between camera and circle
        smart_constraint_create_attach_cam(cam_obj, circle_ctrl)
        
        # Make translate X, Y, Z not-keyable and hide them on circle
        for axis in ['X', 'Y', 'Z']:
            tran_attr = circle_ctrl + ".translate" + axis
            cmds.setAttr(tran_attr, keyable=False)
            cmds.setAttr(tran_attr, channelBox=False)
        
        # Make rotate X, Y, Z not-keyable and hide them on circle
        for axis in ['X', 'Y', 'Z']:
            rot_attr = circle_ctrl + ".rotate" + axis
            cmds.setAttr(rot_attr, keyable=False)
            cmds.setAttr(rot_attr, channelBox=False)
        
        # Animate the locator to match master at each keyframe
        try:
            cmds.refresh(suspend=True)
            cmds.evaluationManager(mode="off")
            cmds.waitCursor(state=True)
            cur_time = cmds.currentTime(q=True)

            for key in keys_time:
                cmds.currentTime(key)
                cmds.matchTransform(loc_ctrl, master_obj, pos=True, rot=True)
                cmds.setKeyframe(loc_ctrl, at=("tx", "ty", "tz", "rx", "ry", "rz"))

            cmds.currentTime(cur_time)
            cmds.refresh(suspend=False)
            cmds.evaluationManager(mode="parallel") 
            cmds.waitCursor(state=False)                           
       
        except Exception as e:
            cmds.refresh(suspend=False)
            cmds.evaluationManager(mode="parallel") 
            cmds.waitCursor(state=False)            
            return
        
        # Set key tangents after all keyframes are created
        cmds.keyTangent(loc_ctrl, at=("tx", "ty", "tz", "rx", "ry", "rz"), itt="auto", ott="step")
        
        # Check if master_obj has keys, if not, add a key to lock its current position
        master_keys = cmds.keyframe(master_obj, query=True, timeChange=True) or []
        if not master_keys:
            print(f"DEBUG: {master_obj} has no keys, adding key at current position")
            cmds.setKeyframe(master_obj, at=("tx", "ty", "tz", "rx", "ry", "rz"))
        
        # Create the constraint between locator and master
        constraints = simple_smart_constraint(loc_ctrl, master_obj, connect_to_attach_cam=True, attach_cam_object=circle_ctrl)
        
        # Always connect to blendParent1 after constraint creation
        if constraints:
            # Check if blendParent1 exists after constraint creation
            if cmds.attributeQuery('blendParent1', node=master_obj, exists=True):
                # If master_obj had no keys, set blendParent1 to 1 (on) first
                if not master_keys:
                    print(f"DEBUG: Setting {master_obj}.blendParent1 to 1 (on) for object with no original keys")
                    cmds.setAttr(f"{master_obj}.blendParent1", 1)
                
                # Connect the Attach_Cam to blendParent1 for all objects
                if cmds.attributeQuery('Attach_Cam', node=circle_ctrl, exists=True):
                    try:
                        print(f"DEBUG: Connecting {circle_ctrl}.Attach_Cam to {master_obj}.blendParent1")
                        cmds.connectAttr(f"{circle_ctrl}.Attach_Cam", f"{master_obj}.blendParent1", force=True)
                        print(f"SUCCESS: Connected {circle_ctrl}.Attach_Cam to {master_obj}.blendParent1")
                    except Exception as e:
                        print(f"ERROR connecting to blendParent1: {e}")
            else:
                print(f"DEBUG: blendParent1 attribute not found on {master_obj}")
        
        print("ATTACH TO CAMERA operation completed!")
    

    cam_row = cmds.rowLayout(
        numberOfColumns=2,
        columnAttach=[(1, 'both', 5), (2, 'both', 5)],
        columnWidth2=(120, 120),
        parent=attach_to_camera_layout
    )
    cmds.button(
        label="Assign Camera",
        command=assign_camera,
        backgroundColor=[0.25, 0.25, 0.25],
        parent=cam_row
    )
    camera_field = cmds.textField(parent=cam_row, backgroundColor=[0.19, 0.19, 0.19])
    

    master_row = cmds.rowLayout(
        numberOfColumns=2,
        columnAttach=[(1, 'both', 5), (2, 'both', 5)],
        columnWidth2=(120, 120),
        parent=attach_to_camera_layout
    )
    cmds.button(
        label="Assign Master Ctrl",
        command=assign_master_ctrl,
        backgroundColor=[0.25, 0.25, 0.25],
        parent=master_row
    )
    master_field = cmds.textField(parent=master_row, backgroundColor=[0.19, 0.19, 0.19])
    

    keys_time_row = cmds.rowLayout(
        numberOfColumns=2,
        columnAttach=[(1, 'both', 5), (2, 'both', 5)],
        columnWidth2=(120, 120),
        parent=attach_to_camera_layout
    )
    cmds.button(
        label="Assign Keys Time",
        command=assign_keys_time,
        backgroundColor=[0.25, 0.25, 0.25],
        parent=keys_time_row
    )
    keys_time_field = cmds.textField(parent=keys_time_row, backgroundColor=[0.19, 0.19, 0.19])    
    
    cmds.separator(height=1, style='none', parent=attach_to_camera_layout)

    cmds.button(
        label="ATTACH TO CAMERA",
        command=attach_to_camera,
        height=35,
        backgroundColor=[0.35, 0.35, 0.35],
        parent=attach_to_camera_layout,
        align="center"
    )
    
    cmds.showWindow(window)


show_ui()