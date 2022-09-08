from dingtalkchatbot.chatbot import DingtalkChatbot


# ===============================
# 发送钉钉消息
# ================
class SendDingTalk:

    def sendDingTalkMsg(self, msg):
        webhook = "https://oapi.dingtalk.com/robot/send?access_token=2c62d40e4ee70f16565ea87e0535f6c8666641a5f3730016588d2c335cc0ee45"
        xiaoding = DingtalkChatbot(webhook)
        xiaoding.send_text(msg="爱设计-" + msg, is_at_all=True)  # 如果钉钉群设置了安全关键词，发消息必须有关键词内容
        return msg
