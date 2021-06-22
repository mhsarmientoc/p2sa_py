#!/bin/bash 
########################################################################
#
# Name          : install.sh
# Purpose       : ancillary functions to install the different project modules
# Arguments     : N/A
#
# History       :       
#
# Created       : March 2018   JPC
########################################################################

# Defining some Maven plugins
#maven_dep_cp_plugin=org.apache.maven.plugins:maven-dependency-plugin:3.0.1:copy
#maven_exec_plugin=org.codehaus.mojo:exec-maven-plugin:1.3.1:exec

########################################
## Get property from any property file
# arg 1: file properties absolute path
# arg 2: property name
########################################
function get_property {
    grep "^$2=" "$1" | cut -d'=' -f2
}

########################################
## Create a tmp dir in case it does not exist
# arg 1: dir absolute path
########################################
function create_temporary_dir {    
   if [ ! -d "$1" ]; then
      mkdir $1
   else
      if [ "$(ls -A $1)" ]; then
        echo "Removing files of $1"
        rm $1/*
      fi
   fi
}

########################################
## remote a tmp dir in case it does  exist
# arg 1: dir absolute path
########################################
function remove_temporary_dir {    
   if [ -d "$1" ]; then
     echo "Removing temporary dir $1";
     rm -rf $1;
   fi
}

########################################
## Copies a package (war/tar..) to a remote server
# arg 1: file to copy
# arg 2: remote path
########################################
function copy_package_to_remote_server {    
  if [ ! -f $1 ]; then
    echo "====> $1 does not exist, installation stops!";
    exit
  fi

  echo "Copying remotely file $1 to $2..."
  scp $1 $2 
}

########################################
## Copies a package (war/tar..) to a local server
# arg 1: file to copy
# arg 2: destination path
########################################
function copy_package_to_local_server {    
  if [ ! -f $1 ]; then
    echo "====> $1 does not exist, installation stops!";
    exit
  fi

  echo "Copying package file $1 to $2..."
  cp $1 $2 
}


########################################
## Retrieves from the properties file the remote dir to install the package
# of the package to copy remotely
# arg 1: properties file path
# arg 2: server_user
# arg 3: server_host
# arg 4: server_instdir
# arg 5: remote_dir
########################################
function retrieve_remote_package_location {    
  eval $2=`get_property $1 server.user`;
  eval $3=`get_property $1 server.host`;
  eval $4=`get_property $1 server.instdir`;

  eval $5="$server_user@$server_host:$server_instdir/"
}
