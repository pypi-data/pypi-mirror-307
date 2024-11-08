#!/bin/bash

# 变量初始化
new_user=$1
PASSWD=$2

# 设置颜色
setup_color() {
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

log_file="linklinux_env_log"

# 配置 sshd
configure_sshd() {
    echo "${YELLOW}配置 SSHD 中...${RESET}"
    sed -i 's/#ClientAliveInterval 0/ClientAliveInterval 60/' /etc/ssh/sshd_config
    sed -i 's/#ClientAliveCountMax 3/ClientAliveCountMax 3/' /etc/ssh/sshd_config
    sudo service sshd restart
    echo "${GREEN}SSHD 配置成功${RESET}"
}

# 安装 vim
install_vim() {
    echo "${YELLOW}配置 vim 中...${RESET}" >> $log_file
    if [ -f "/home/$new_user/install_vim.sh" ]; then
        echo "install_vim.sh 文件已存在，已删除"
        rm -f /home/$new_user/install_vim.sh*
    fi
    wget 182.92.157.34:88/install_vim.sh -O /home/$new_user/install_vim.sh
    bash /home/$new_user/install_vim.sh
    echo "${GREEN}配置 vim 成功${RESET}" >> $log_file
}

# 安装 zsh
install_zsh() {
    echo "${YELLOW}配置 zsh 中...${RESET}" >> $log_file
    if [ -f "/home/$new_user/install_zsh.sh" ]; then
        echo "install_zsh.sh 文件已存在，已删除"
        rm -f /home/$new_user/install_zsh.sh*
    fi
    cp install_zsh.sh /home/$new_user/install_zsh.sh
    bash /home/$new_user/install_zsh.sh ${PASSWD}
    echo "${GREEN}配置 zsh 成功${RESET}" >> $log_file

    # 安装 zsh 插件
    git clone https://gitee.com/suyelu/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
    sed -i 's/plugins=(git)/plugins=(git zsh-syntax-highlighting)/' ~/.zshrc
    echo "${GREEN}zsh-syntax-highlighting 插件安装成功，内容替换完成${RESET}" >> $log_file
}

# 安装自动补全插件
autocomplete_plugin() {
    echo "${YELLOW}配置自动补全插件中...${RESET}" >> $log_file
    mkdir -p ~/.oh-my-zsh/plugins/incr
    wget http://123.57.201.194/data/incr-0.2.zsh -O ~/.oh-my-zsh/plugins/incr/incr.plugin.zsh
    echo "source ~/.oh-my-zsh/plugins/incr/incr*.zsh" >> ~/.zshrc
    echo "${GREEN}自动补全插件配置成功${RESET}" >> $log_file
}

# 配置目录跳转插件
configure_autojump() {
    echo "${YELLOW}配置目录跳转插件中...${RESET}" >> $log_file
    echo 'autoload -U colors && colors'  >> ~/.zshrc
    echo 'PROMPT="%{$fg[red]%}%n%{$reset_color%}@%{$fg[blue]%}%m %{$fg[yellow]%}%1~ %{$reset_color%}%# "' >> ~/.zshrc
    echo 'RPROMPT="[%{$fg[yellow]%}%?%{$reset_color%}]"' >> ~/.zshrc
    echo '[ -r "/etc/zshrc_$TERM_PROGRAM" ] && . "/etc/zshrc_$TERM_PROGRAM"' >> ~/.zshrc
    echo 'source /usr/share/autojump/autojump.sh' >> ~/.zshrc
    echo "${GREEN}目录跳转插件配置成功${RESET}" >> $log_file
}

# 配置 ctags
configure_ctags() {
    ctags -I __THROW -I __attribute_pure__ -I __nonnull -I __attribute__ --file-scope=yes --langmap=c:+.h --languages=c,c++ --links=yes --c-kinds=+p --c++-kinds=+p --fields=+iaS --extra=+q -R -f ~/.vim/systags /usr/include/ /usr/local/include
    echo 'set tags+=~/.vim/systags' >> ~/.vimrc
    echo "${GREEN}ctags 配置成功${RESET}" >> $log_file
}

# 下载并设置 isoftstone_check
setup_isoftstone_check() {
    echo "${YELLOW}配置云主机检测工具中...${RESET}"
    if [[ `uname -m` == x86* ]]; then
        wget http://123.57.201.194/data/kkb_check_ubuntu_18.04 -O isoftstone_check
    else
        wget http://123.57.201.194/data/kkb_check_ubuntu_18.04_arm -O isoftstone_check
    fi
    chmod a+x isoftstone_check
    sudo mv isoftstone_check /usr/bin
    echo "${GREEN}云主机检测工具配置成功${RESET}"
}

# 执行各个步骤
configure_sshd
install_vim
install_zsh
autocomplete_plugin
configure_autojump
configure_ctags
#setup_isoftstone_check

# 清理临时文件
rm -f $log_file

echo "${GREEN}你的主机配置完成，请重新连接到主机开始使用${RESET}"
exit

