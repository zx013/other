#-*- coding:utf-8 -*-

#主要信号类型
#CLOCK_EVENT, BUFF_EVENT, DEVICE_EVENT

#次要信号类型
#CLOCK_EVENT->时间戳
#BUFF_EVENT -> type -> ['in', 'body', 'out']->['before', 'after']
#DEVICE_EVENT -> type -> key


#ACTION(BUFF) -> EVENT -> BUFF

#CLOCK -> CLOCK_EVENT -> MAIN_BUFF -> BUFF_EVENT -> BUFF

#BUFF只有捕获到了对应的EVENT，才执行相关的动作

#OBJECT
#BUFF
#OBJECT相互作用生成BUFF
#BUFF附属于OBJECT
#BUFF创建或操作OBJECT

#关联OBJECT
#OBJECT和其它OBJECT关联，该OBJECT主动碰撞时影响到关联OBJECT