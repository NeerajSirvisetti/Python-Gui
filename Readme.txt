

#################
Version 1.0
################
1. Created boxes based on the steps given 
2. Once selected a box, that box turned to Yellow color upon selection.
3. Introduced bind keys for exiting the gui_application.



#################
Version 1.1
#################
The functionality of a class that continously checks a folder , if in the folder certain named file is present then that named step box should be changed to green color, then if the box color is green then even if we press the box just we need to get message saying that already action completed.

Info:
To achieve the functionality of continuously checking a folder for a specific file and updating the corresponding step box color, you can create a separate class for the folder monitoring task and integrate it with your GUI class. Additionally, you can add a mechanism to track whether an action has already been completed and display a message accordingly. 

New changes introduced:
1. Added a FileChecker class that continuously monitors a specified folder for the presence of certain files.
2. The ff_gui class is modified to create an instance of FileChecker and start monitoring the folder.
3. The on_key_Init method now simulates an action for the 'Init' step and updates the box color to green. It also tracks whether the action has already been completed.
4. The on_box_select method checks whether the action for the selected step has already been completed and updates the label accordingly.
The execute_function method updates the action completion status and the box color to green.

#################
Version 1.2 (Major update)
#################
1) when User select the box which was previously not have green color, it should perform certain function then turn into yellow for 3 secs later get back to green color. 
2) when user select the box which is already green then get message saying this action is already done.
3) The message which every is displayed should be only visible for 3 secs and then dissapear after showing.
4) The message panel of the above operations should be of white background like a separate message box with black font and should be present below the last step box 

Info: 
The changes include the addition of a message panel below the last step box, handling the selection of boxes differently based on their color, and displaying messages for a limited time. 

New changes introduced:
1. A message_label is added to display messages at the bottom of the window.
The display_message method is created to set the message text, display it for 3 seconds, and then clear the message.
2. The on_box_select method is modified to perform an additional action when selecting a box that was not green previously. The box turns yellow for 3 seconds and then back to green.
3. The perform_additional_action method is a placeholder for the actual function you want to execute when selecting a box that was not green previously. Replace it with your specific logic.

############
version 1.3
############
Executing the shell commands based on the step that is selected

Info: 
If you want to execute a shell command in the background when a box is selected (which is not green), you can use the subprocess module to run the command asynchronously.

New changes introduced:
1. The execute_command_for_step method is added to execute a shell command for the given step. The subprocess.run function is used to run the command in the background.
2. The on_key_Init method is updated to call execute_command_for_step to simulate executing a command for the 'Init' step.
3. The on_box_select method is updated to call execute_command_for_step when selecting a box that is not green.
4. The Thread is used to run the command in the background, preventing it from blocking the GUI.

##############
Version 1.4 
###############
Introducing a bind key for restarting the application

Info:
Introduce a key binding to rerun the whole code.

New changes introduced:
1. The on_key_restart method is added to handle the "Ctrl+R" key combination. It displays a message and then calls the restart_application method.
2. The restart_application method restarts the application by calling os.execl with the current Python executable and script arguments.
3. You can press "Ctrl+R" to restart the application.



###################
Version 2.0
###################
To have the following modifications:
1. The steps should be now be able to be selected in form of drop down.
2. Once one step is selected from the drop down there need to be 2 buttons beside the step, 1. Run 2.Stop; once run is pressed then it needs to execute the shell command that is associated with the step selected as per before code, if stop selected then the shell command that is currently running need to be stopped. The stop key need to be able to press only when the run key is pressed and the command is being ingoing in shell, if not it should be in inactive state with different color without able to be pressed.
3. The steps should be now only visible based on the drop down selected.
4. One new message window need to be there for Completed Steps.The steps which are of green color like of before code logic then it should display in this new window as names or small blocks .
5. The Message window which was already existing in the code need to be now displayed below the above in new message window. 
6. Fit to the screen based on the dimension.




###################
Version 2.1
###################
To have the following modifications:
1. The drop down selection color should be different based on the completion.
2. Allign the message window below the completed steps section.
3. If the selected step is run, previous steps should also be ran if not greeen or completed and then at last run the selected step.


###################
Experimental files
###################
bindkeys.py -> for integrating bindkeys into gui , based on selection certain operations to execute.
checker.py -> continuously checks for something based on what is mentioned or stated, then perform certain task based on certain conditions.
