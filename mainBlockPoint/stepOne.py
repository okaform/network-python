#Threading with 5 at a time
#find a test for 9200 and 9200L
#regex for bytes free to compare with size of image  
import subprocess


#step one for all the 9(2-5)XX's
def remove(con_from_main): 
    remove_cmd = "install remove inactive"
    ver = con_from_main.send_command_timing(remove_cmd, read_timeout=0, last_read = 12.0)
    print(ver)
    
    
    
def copy_new_image(con_from_main):
    tftp_server = "10.59.254.7"
    version_name = ""
    #determine the version and depending on it, push the image
    get_version_cmd = con_from_main.send_command("sh ver | sec cisco C")
    if "9300" in get_version_cmd:
        version_name = "9300"
        copy_image_cmd = "copy tftp://"+tftp_server+"/ios/current/cat9k_lite_iosxe.17.06.04.SPA.bin flash:"
        print(con_from_main.send_command_timing(copy_image_cmd, read_timeout=0, last_read = 12.0))
        con_from_main.send_command_timing("")
    elif "9500" in get_version_cmd:
        version_name = "9500"
        copy_image_cmd = "copy tftp://"+tftp_server+"/ios/current/cat9k_lite_iosxe.17.06.04.SPA.bin flash:"
        print(con_from_main.send_command_timing(copy_image_cmd, read_timeout=0, last_read = 12.0))
    elif "9200L" in get_version_cmd:
        version_name = "9200L"
        copy_image_cmd = "copy tftp://"+tftp_server+"/ios/current/cat9k_lite_iosxe.17.06.04.SPA.bin flash:"
        print(con_from_main.send_command_timing(copy_image_cmd, read_timeout=0, last_read = 12.0))
        print("This is 9200L")
    elif "9200" in get_version_cmd:
        version_name = "9200"
        print("This is 9200")
        copy_image_cmd = "copy tftp://"+tftp_server+"/ios/current/cat9k_lite_iosxe.17.06.04.SPA.bin flash:"
        print(con_from_main.send_command_timing(copy_image_cmd, read_timeout=0, last_read = 12.0))
    else:
        print("This version is not supported in this script. Please try manually.")
        copy_image_cmd = "copy tftp://"+tftp_server+"/ios/current/cat9k_lite_iosxe.17.06.04.SPA.bin flash:"
        copying =  con_from_main.send_command_timing(copy_image_cmd)
        print(copying)
        print(con_from_main.send_command_timing(" ", read_timeout=0, last_read = 12.0, delay_factor=1))
        return version_name
        
    return version_name
        #copy_image_cmd = "copy tftp://"+tftp_server+"/ios/current/cat9k_lite_iosxe.17.06.04.SPA.bin flash:"
        #print(con_from_main.send_command_timing(copy_image_cmd, read_timeout=0, last_read = 12.0))
        #con_from_main.send_command_timing("")    
    
    
    
    

