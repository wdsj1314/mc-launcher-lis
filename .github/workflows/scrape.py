import json

data = [
    {
        "name":"ZL2(ZalithLauncher)",
        "homepage":"https://github.com/Andrew2169/ZalithLauncher",
        "type":"mobile"
    },
    {
        "name":"FCL(FoldCraft Launcher)",
        "homepage":"https://github.com/FCL-Team/FoldCraftLauncher",
        "type":"mobile"
    },
    {
        "name":"PojavLauncher(原版手机)",
        "homepage":"https://github.com/PojavLauncherTeam/PojavLauncher",
        "type":"mobile"
    },
    {
        "name":"FlintLauncher",
        "homepage":"https://github.com/FlintLauncher/FlintLauncher",
        "type":"mobile"
    },
    {
        "name":"MidnightLauncher",
        "homepage":"https://github.com/Midnight-Launcher/MidnightLauncher",
        "type":"mobile"
    },
    {
        "name":"Amethyst",
        "homepage":"https://github.com/Amethyst-MC/Amethyst",
        "type":"mobile"
    },
    {
        "name":"美西螈启动器 Axolotl Launcher",
        "homepage":"https://axolotllauncher.top",
        "type":"mobile"
    },
    {
        "name":"PCL2(Windows)",
        "homepage":"https://github.com/HuangHongPC/PCL2",
        "type":"pc"
    },
    {
        "name":"HMCL3(全平台)",
        "homepage":"https://github.com/huanghongxun/HMCL",
        "type":"pc"
    },
    {
        "name":"Prism Launcher",
        "homepage":"https://github.com/PrismLauncher/PrismLauncher",
        "type":"pc"
    },
    {
        "name":"MultiMC",
        "homepage":"https://github.com/MultiMC/Launcher",
        "type":"pc"
    },
    {
        "name":"ATLauncher",
        "homepage":"https://www.atlauncher.com",
        "type":"pc"
    },
    {
        "name":"Modrinth App",
        "homepage":"https://modrinth.com/app",
        "type":"pc"
    },
    {
        "name":"Minecraft官方启动器",
        "homepage":"https://www.minecraft.net/zh-hd/download",
        "type":"pc"
    }
]

with open("list.json","w",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False,indent=2)

