#!/bin/bash 
echo "What is your First name"
read Firstname
echo "What is your Last name"
read Lastname
echo "Your name is $Firstname $Lastname"
if[ !$Firstname = !$Lastname ]
    then echo "Welcome $Firstname $Lastname"
elif [ $Firstname = !$Lastname ]
    then echo "Error"
else echo "Goodbye"
fi
case [] :
