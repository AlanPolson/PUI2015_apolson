# Windows 8 Environment setup instructions:

To set up the alias in my Windows 8 machine, I took the following steps:

1)Create environmental variable:

export PUI2015="C:/\users/\christeen/\desktop/\Alan_Polson/\Other/\CUSP/\PUI2015

2) create a .bashrc file

touch .bashrc

3) edit the bashrc file and create an alias in it

vim .bashrc

	add the below line in vim: 

	alias pui2015='cd $PUI2015'

(if you are unfamiliar with vim, you basically add the line by pressing 'i', typing in the line, then pressing 'esc', followed by ':', 'w', 'q' and 'enter')

4) run the alias in .bashrc

source:bashrc

5)Testing

Here is a screenshot of my alias in action:


