#!/bin/bash

setup_color() {
    # Only use colors if connected to a terminal
    if [ -t 1 ]; then
        RED=$(printf '\033[31m')
        GREEN=$(printf '\033[32m')
        YELLOW=$(printf '\033[33m')
        BLUE=$(printf '\033[34m')
        BOLD=$(printf '\033[1m')
        RESET=$(printf '\033[m')
    else
        RED=""
        GREEN=""
        YELLOW=""
        BLUE=""
        BOLD=""
        RESET=""
    fi
}

setup_color

username=`whoami`
if [[ ! ${username} == "root" ]];then
    echo "${RED}请使用root用户执行该脚本${RESET}"
    exit
fi

# 1. 询问是否修改当前主机的名字
echo "当前主机名为: $(hostname)"
echo "${BOLD}请选择是否修改主机名:${RESET}"
echo "1) 是"
echo "2) 否"
read -p "${BLUE}请输入选项${RESET} (${YELLOW}1/2${RESET}): " change_hostname
if [[ ${change_hostname} == "1" ]]; then
    regex="^[a-zA-Z]+$"
    while [[ 1 ]]; do
        read -p "请为你的云主机设置一个${RED}主机名字${RESET}(${YELLOW}纯英文${RESET}): " host_name
        if [[ ! ${host_name} =~ ${regex} ]]; then
            echo "${RED}您的主机名不符合规则，请重新输入${RESET}"
            continue
        else
            break
        fi
    done
    if [[ "$(uname)" == "Darwin" ]]; then
        scutil --set HostName ${host_name}
    else
        hostnamectl set-hostname ${host_name}
    fi
echo "${GREEN}主机名已成功修改为${RESET} ${host_name}"
    echo "名字切换完成"
fi

# 更新 /etc/hosts 文件
if [[ "$(uname)" == "Darwin" ]]; then
    host_ip=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
else
    host_ip=$(hostname -I | awk '{print $1}')
fi
host_entry_exists=$(grep -n "${host_ip}" /etc/hosts | head -1 | awk -F':' '{print $1}')
if [ ! -n "${host_entry_exists}" ]; then
    echo "${YELLOW}未查询到主机名，正在尾部追加数据...${RESET}"
    echo "${host_ip}\t${host_name}\t${host_name}" >> /etc/hosts
else
    echo "${YELLOW}已查询到主机名，正在替换文件内容...${RESET}"
    host_entry_tmp="${host_ip}\t${host_name}\t${host_name}"
    if [[ "$(uname)" == "Darwin" ]]; then
        sed -i '' "${host_entry_exists}s/.*/${host_entry_tmp}/" /etc/hosts
    else
        sed -i "${host_entry_exists}s/.*/${host_entry_tmp}/" /etc/hosts
    fi
fi

# 2. 列出当前已经有的用户名，并询问操作
echo "当前已有的用户名:"
if [[ "$(uname)" == "Darwin" ]]; then
    users=( $(dscl . list /Users | grep -v '^_' | grep -v daemon | grep -v nobody) root )
else
    users=( $(awk -F: '$3 >= 1000 && $3 < 65534 {print $1}' /etc/passwd) root )
fi
for i in "${!users[@]}"; do
    echo "${YELLOW}$((i+1))${RESET}) ${BLUE}${users[$i]}${RESET}"
done

echo "请选择操作:"
echo "1) 修改现有用户的配置"
echo "2) 新增用户并做初始化配置"
read -p "${BLUE}请输入选项${RESET} (${YELLOW}1/2${RESET}): " user_action

if [[ ${user_action} == "1" ]]; then
    echo "${BOLD}请选择要修改的用户编号:${RESET}"
read -p "${BLUE}请输入用户编号${RESET} (${YELLOW}1-${#users[@]}${RESET}): " user_number
    if (( user_number >= 1 && user_number <= ${#users[@]} )); then
        username=${users[$((user_number-1))]}
    else
        echo "${RED}无效的用户编号，请检查输入是否正确。${RESET}"
        exit 1
    fi
elif [[ ${user_action} == "2" ]]; then
    regex="^[a-zA-Z]+$"
    while [[ 1 ]]; do
        read -p "${BLUE}请输入你的用户名${RESET}（${YELLOW}必须英文${RESET}）: " username
        if [[ ! ${username} =~ ${regex} ]]; then
            echo "${RED}您的用户名不符合规则，请重新输入${RESET}"
            continue
        else
            break
        fi
    done

    while [[ 1 ]]; do
        read -p "${BLUE}请为用户 ${username} 设置一个密码${RESET}: " USER_PASSWD
        read -p "${BLUE}你的密码为${RESET} ${GREEN}${USER_PASSWD}${RESET}, ${YELLOW}请输入 y 确认${RESET}, 其他任何字符将重新设置密码 [y/n]: " in_tmp
        if [[ ${in_tmp} == 'y' ]]; then
            break
        else
            continue
        fi
    done

    echo "${YELLOW}正在添加用户${RESET} ${username}..."
useradd ${username} -G sudo -m && echo "${GREEN}用户添加成功${RESET}" || ( userdel -rf ${username}; echo "${RED}已删除现有用户${RESET} ${username}" && useradd ${username} -G sudo -m && echo "${GREEN}用户添加成功${RESET}" )

    sleep 1
    (
        sleep 1
        echo ${USER_PASSWD}
        sleep 1
        echo ${USER_PASSWD}
    ) | passwd ${username}

    if [ $? -eq 0 ]; then
        echo "${GREEN}密码修改成功${RESET}"
    else
        echo "${RED}密码修改失败${RESET}"
        exit
    fi

    echo "${GREEN}用户配置已完成${RESET}"
fi

# 下载并配置 linklinux_env.sh
cp linklinux_env.sh /home/${username}/
chown ${username} /home/${username}/linklinux_env.sh
chgrp ${username} /home/${username}/linklinux_env.sh
chmod a+x /home/${username}/linklinux_env.sh

# 修改 sudoers 文件，允许新用户使用 sudo 而无需密码
q=$(grep -n '%sudo\tALL=(ALL:ALL) ALL' /etc/sudoers | awk -F':' '{print $1}')
if [ ! -n "$q" ]; then
    echo "${YELLOW}正在修改 sudo 命令权限...${RESET}"
else
    TMPq='%sudo\tALL=(ALL:ALL) NOPASSWD: ALL'
    sed -i "$q c $TMPq" /etc/sudoers
    echo "${GREEN}sudo 权限已修改完成${RESET}"
fi

# 执行用户环境配置脚本
su - ${username} -c "bash linklinux_env.sh ${username} ${USER_PASSWD}"

# 恢复 sudoers 文件
l=$(grep -n '%sudo\tALL=(ALL:ALL) NOPASSWD: ALL' /etc/sudoers | awk -F':' '{print $1}')
if [ -n "$l" ]; then
    TMPl='%sudo\tALL=(ALL:ALL) ALL'
    sudo sed -i "$l c $TMPl" /etc/sudoers
    echo "${GREEN}sudo 内容已恢复${RESET}"
fi

# 清理临时文件
cd
rm ./init_env.sh
rm ./linklinux_env.sh

echo -e "${GREEN}你的用户名${RESET} ${BLUE}${username}${RESET}, ${GREEN}密码为${RESET} ${USER_PASSWD}
${YELLOW}请使用新用户登录系统${RESET}"

su - ${username}

