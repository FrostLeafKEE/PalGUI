"""幻兽帕鲁服务器配置项元数据定义。

所有配置项的结构化描述，包括类型、默认值、取值范围、中文标签和分组信息。
该模块定义了 UI 表单生成所需的一切元数据。
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConfigType(Enum):
    """配置项数据类型"""
    BOOL = "bool"
    FLOAT = "float"
    INT = "int"
    STRING = "string"
    ENUM = "enum"


@dataclass
class ConfigItem:
    """单个配置项的元数据"""
    key: str                          # 配置变量名（如 DayTimeSpeedRate）
    label_cn: str                     # 中文标签
    group: str                        # 分组名称
    config_type: ConfigType           # 数据类型
    default: Any                      # 默认值
    description: str = ""             # 详细描述/注释
    min_val: float | None = None      # 数值型最小值
    max_val: float | None = None      # 数值型最大值
    step: float = 1.0                 # 数值型步长
    decimals: int = 6                 # 浮点型小数位数
    options: list[str] | None = None  # 枚举型可选值列表
    password: bool = False            # 是否为密码字段


# ============================================================
# 配置项完整定义（按分组排列）
# ============================================================

CONFIG_SCHEMA: list[ConfigItem] = [
    # ==================== 难度与随机化 ====================
    ConfigItem(
        key="Difficulty", label_cn="难度", group="难度与随机化",
        config_type=ConfigType.ENUM, default="None",
        options=["None", "Casual", "Normal", "Hard"],
        description="游戏难度（None=无/Casual=休闲/Normal=普通/Hard=困难）",
    ),
    ConfigItem(
        key="RandomizerType", label_cn="随机化类型", group="难度与随机化",
        config_type=ConfigType.STRING, default="None",
        description="随机化类型（None=无）",
    ),
    ConfigItem(
        key="RandomizerSeed", label_cn="随机化种子", group="难度与随机化",
        config_type=ConfigType.STRING, default="",
        description="随机化种子值，留空为随机",
    ),
    ConfigItem(
        key="bIsRandomizerPalLevelRandom", label_cn="随机化帕鲁等级", group="难度与随机化",
        config_type=ConfigType.BOOL, default=False,
        description="是否随机化帕鲁等级",
    ),

    # ==================== 时间流速 ====================
    ConfigItem(
        key="DayTimeSpeedRate", label_cn="白天时间流速", group="时间流速",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.1, max_val=10.0, step=0.1, decimals=6,
        description="白天时间流逝速度倍率",
    ),
    ConfigItem(
        key="NightTimeSpeedRate", label_cn="夜晚时间流速", group="时间流速",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.1, max_val=10.0, step=0.1, decimals=6,
        description="夜晚时间流逝速度倍率",
    ),

    # ==================== 经验与捕获 ====================
    ConfigItem(
        key="ExpRate", label_cn="经验倍率", group="经验与捕获",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="经验获取倍率",
    ),
    ConfigItem(
        key="PalCaptureRate", label_cn="帕鲁捕获倍率", group="经验与捕获",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="帕鲁捕获成功率倍率",
    ),
    ConfigItem(
        key="PalSpawnNumRate", label_cn="帕鲁生成数量倍率", group="经验与捕获",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="帕鲁生成数量倍率",
    ),

    # ==================== 伤害倍率 ====================
    ConfigItem(
        key="PalDamageRateAttack", label_cn="帕鲁攻击伤害倍率", group="伤害倍率",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="帕鲁对目标造成的伤害倍率",
    ),
    ConfigItem(
        key="PalDamageRateDefense", label_cn="帕鲁防御倍率", group="伤害倍率",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="帕鲁受到的伤害倍率（越大受伤越重）",
    ),
    ConfigItem(
        key="PlayerDamageRateAttack", label_cn="玩家攻击伤害倍率", group="伤害倍率",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="玩家对目标造成的伤害倍率",
    ),
    ConfigItem(
        key="PlayerDamageRateDefense", label_cn="玩家防御倍率", group="伤害倍率",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="玩家受到的伤害倍率（越大受伤越重）",
    ),

    # ==================== 玩家状态消耗 ====================
    ConfigItem(
        key="PlayerStomachDecreaceRate", label_cn="玩家饱食度消耗速度", group="玩家状态消耗",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="玩家饱食度下降速度倍率",
    ),
    ConfigItem(
        key="PlayerStaminaDecreaceRate", label_cn="玩家体力消耗速度", group="玩家状态消耗",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="玩家体力下降速度倍率",
    ),
    ConfigItem(
        key="PlayerAutoHPRegeneRate", label_cn="玩家自动生命恢复速度", group="玩家状态消耗",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="玩家自动回血速度倍率",
    ),
    ConfigItem(
        key="PlayerAutoHpRegeneRateInSleep", label_cn="玩家睡眠生命恢复速度", group="玩家状态消耗",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="玩家睡眠时回血速度倍率",
    ),

    # ==================== 帕鲁状态消耗 ====================
    ConfigItem(
        key="PalStomachDecreaceRate", label_cn="帕鲁饱食度消耗速度", group="帕鲁状态消耗",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="帕鲁饱食度下降速度倍率",
    ),
    ConfigItem(
        key="PalStaminaDecreaceRate", label_cn="帕鲁体力消耗速度", group="帕鲁状态消耗",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="帕鲁体力下降速度倍率",
    ),
    ConfigItem(
        key="PalAutoHPRegeneRate", label_cn="帕鲁自动生命恢复速度", group="帕鲁状态消耗",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="帕鲁自动回血速度倍率",
    ),
    ConfigItem(
        key="PalAutoHpRegeneRateInSleep", label_cn="帕鲁睡眠生命恢复速度", group="帕鲁状态消耗",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="帕鲁睡眠时回血速度倍率",
    ),

    # ==================== 建筑相关 ====================
    ConfigItem(
        key="BuildObjectHpRate", label_cn="建筑生命值倍率", group="建筑相关",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="建筑生命值倍率",
    ),
    ConfigItem(
        key="BuildObjectDamageRate", label_cn="建筑受到伤害倍率", group="建筑相关",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="建筑受到伤害的倍率",
    ),
    ConfigItem(
        key="BuildObjectDeteriorationDamageRate", label_cn="建筑风化劣化伤害倍率", group="建筑相关",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="建筑随时间劣化的伤害倍率",
    ),

    # ==================== 采集与掉落 ====================
    ConfigItem(
        key="CollectionDropRate", label_cn="采集掉落倍率", group="采集与掉落",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="采集资源时的掉落倍率",
    ),
    ConfigItem(
        key="CollectionObjectHpRate", label_cn="采集物生命值倍率", group="采集与掉落",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="采集物（矿、树等）生命值倍率",
    ),
    ConfigItem(
        key="CollectionObjectRespawnSpeedRate", label_cn="采集物刷新速度倍率", group="采集与掉落",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="采集物重新生成速度倍率",
    ),
    ConfigItem(
        key="EnemyDropItemRate", label_cn="敌人掉落物品倍率", group="采集与掉落",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="击败敌人时的物品掉率倍率",
    ),

    # ==================== 死亡惩罚 ====================
    ConfigItem(
        key="DeathPenalty", label_cn="死亡惩罚", group="死亡惩罚",
        config_type=ConfigType.ENUM, default="Item",
        options=["None", "Item", "All"],
        description="死亡惩罚类型（None=无掉落/Item=掉落物品/All=全部掉落）",
    ),

    # ==================== 玩家互动 ====================
    ConfigItem(
        key="bEnablePlayerToPlayerDamage", label_cn="启用玩家对玩家伤害", group="玩家互动",
        config_type=ConfigType.BOOL, default=False,
        description="是否允许玩家之间互相造成伤害",
    ),
    ConfigItem(
        key="bEnableFriendlyFire", label_cn="启用友军伤害", group="玩家互动",
        config_type=ConfigType.BOOL, default=False,
        description="是否允许友军之间互相伤害",
    ),
    ConfigItem(
        key="bEnableInvaderEnemy", label_cn="启用入侵敌人", group="玩家互动",
        config_type=ConfigType.BOOL, default=True,
        description="是否允许敌人入侵基地事件",
    ),
    ConfigItem(
        key="bActiveUNKO", label_cn="启用粪便功能", group="玩家互动",
        config_type=ConfigType.BOOL, default=False,
        description="是否启用帕鲁粪便功能",
    ),
    ConfigItem(
        key="bEnableAimAssistPad", label_cn="启用手柄瞄准辅助", group="玩家互动",
        config_type=ConfigType.BOOL, default=True,
        description="手柄玩家是否启用瞄准辅助",
    ),
    ConfigItem(
        key="bEnableAimAssistKeyboard", label_cn="启用键盘瞄准辅助", group="玩家互动",
        config_type=ConfigType.BOOL, default=False,
        description="键鼠玩家是否启用瞄准辅助",
    ),

    # ==================== 掉落物品限制 ====================
    ConfigItem(
        key="DropItemMaxNum", label_cn="最大掉落物品数量", group="掉落物品限制",
        config_type=ConfigType.INT, default=3000,
        min_val=0, max_val=100000, step=1,
        description="地图上同时存在的最大掉落物品数量",
    ),
    ConfigItem(
        key="PhysicsActiveDropItemMaxNum", label_cn="物理激活掉落物品最大数", group="掉落物品限制",
        config_type=ConfigType.INT, default=-1,
        min_val=-1, max_val=100000, step=1,
        description="具有物理效果的掉落物品最大数量（-1=无限制）",
    ),
    ConfigItem(
        key="DropItemMaxNum_UNKO", label_cn="粪便最大数量", group="掉落物品限制",
        config_type=ConfigType.INT, default=100,
        min_val=0, max_val=10000, step=1,
        description="地图上最大粪便数量",
    ),
    ConfigItem(
        key="DropItemAliveMaxHours", label_cn="掉落物品存活时间（小时）", group="掉落物品限制",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=168.0, step=0.1, decimals=6,
        description="掉落物品在消失前的最大存活小时数",
    ),

    # ==================== 基地与公会 ====================
    ConfigItem(
        key="BaseCampMaxNum", label_cn="最大基地数量", group="基地与公会",
        config_type=ConfigType.INT, default=128,
        min_val=1, max_val=1000, step=1,
        description="服务器中最大基地总数",
    ),
    ConfigItem(
        key="BaseCampWorkerMaxNum", label_cn="每基地最大工作帕鲁数", group="基地与公会",
        config_type=ConfigType.INT, default=15,
        min_val=1, max_val=100, step=1,
        description="每个基地最大可工作的帕鲁数量",
    ),
    ConfigItem(
        key="AutoResetGuildTimeNoOnlinePlayers", label_cn="公会无人在线自动重置时间", group="基地与公会",
        config_type=ConfigType.FLOAT, default=72.0,
        min_val=0.0, max_val=8760.0, step=1.0, decimals=6,
        description="公会所有成员离线多久后自动重置（小时）",
    ),
    ConfigItem(
        key="bAutoResetGuildNoOnlinePlayers", label_cn="自动重置无人在线公会", group="基地与公会",
        config_type=ConfigType.BOOL, default=False,
        description="是否自动重置没有在线玩家的公会",
    ),
    ConfigItem(
        key="GuildPlayerMaxNum", label_cn="公会最大玩家数", group="基地与公会",
        config_type=ConfigType.INT, default=20,
        min_val=1, max_val=200, step=1,
        description="每个公会的最大玩家数量",
    ),
    ConfigItem(
        key="BaseCampMaxNumInGuild", label_cn="公会最大基地数量", group="基地与公会",
        config_type=ConfigType.INT, default=4,
        min_val=1, max_val=100, step=1,
        description="每个公会允许的最大基地数量",
    ),

    # ==================== 孵化 ====================
    ConfigItem(
        key="PalEggDefaultHatchingTime", label_cn="帕鲁蛋孵化时间倍率", group="孵化",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="帕鲁蛋默认孵化所需时间倍率",
    ),

    # ==================== 工作速度 ====================
    ConfigItem(
        key="WorkSpeedRate", label_cn="工作速度倍率", group="工作速度",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=100.0, step=0.1, decimals=6,
        description="帕鲁工作速度倍率",
    ),

    # ==================== 保存 ====================
    ConfigItem(
        key="AutoSaveSpan", label_cn="自动保存间隔（秒）", group="保存",
        config_type=ConfigType.FLOAT, default=30.0,
        min_val=10.0, max_val=3600.0, step=10.0, decimals=6,
        description="服务器自动保存间隔时间",
    ),

    # ==================== 多人/PvP/硬核模式 ====================
    ConfigItem(
        key="bIsMultiplay", label_cn="启用多人模式", group="多人/PvP/硬核模式",
        config_type=ConfigType.BOOL, default=False,
        description="是否启用多人游戏模式",
    ),
    ConfigItem(
        key="bIsPvP", label_cn="启用PvP", group="多人/PvP/硬核模式",
        config_type=ConfigType.BOOL, default=False,
        description="是否开启玩家间对战",
    ),
    ConfigItem(
        key="bHardcore", label_cn="启用硬核模式", group="多人/PvP/硬核模式",
        config_type=ConfigType.BOOL, default=False,
        description="是否启用硬核（死亡永久）模式",
    ),
    ConfigItem(
        key="bPalLost", label_cn="帕鲁死亡消失", group="多人/PvP/硬核模式",
        config_type=ConfigType.BOOL, default=False,
        description="帕鲁死亡后是否永久消失（硬核相关）",
    ),
    ConfigItem(
        key="bCharacterRecreateInHardcore", label_cn="硬核模式允许重建角色", group="多人/PvP/硬核模式",
        config_type=ConfigType.BOOL, default=False,
        description="硬核模式下是否允许重新创建角色",
    ),
    ConfigItem(
        key="bCanPickupOtherGuildDeathPenaltyDrop", label_cn="拾取其他公会死亡掉落", group="多人/PvP/硬核模式",
        config_type=ConfigType.BOOL, default=False,
        description="是否允许拾取其他公会玩家的死亡掉落物品",
    ),
    ConfigItem(
        key="bEnableNonLoginPenalty", label_cn="启用未登录惩罚", group="多人/PvP/硬核模式",
        config_type=ConfigType.BOOL, default=True,
        description="是否对长期未登录玩家启用惩罚机制",
    ),

    # ==================== 传送与地图 ====================
    ConfigItem(
        key="bEnableFastTravel", label_cn="启用快速传送", group="传送与地图",
        config_type=ConfigType.BOOL, default=True,
        description="是否允许快速传送",
    ),
    ConfigItem(
        key="bEnableFastTravelOnlyBaseCamp", label_cn="仅限基地快速传送", group="传送与地图",
        config_type=ConfigType.BOOL, default=False,
        description="快速传送是否仅限于基地之间",
    ),
    ConfigItem(
        key="bIsStartLocationSelectByMap", label_cn="通过地图选择出生点", group="传送与地图",
        config_type=ConfigType.BOOL, default=False,
        description="是否允许玩家通过地图选择出生位置",
    ),

    # ==================== 其他玩家/公会可见性 ====================
    ConfigItem(
        key="bExistPlayerAfterLogout", label_cn="玩家登出后保留在游戏中", group="可见性",
        config_type=ConfigType.BOOL, default=False,
        description="玩家登出后其角色是否仍留在游戏世界",
    ),
    ConfigItem(
        key="bEnableDefenseOtherGuildPlayer", label_cn="允许防御其他公会玩家", group="可见性",
        config_type=ConfigType.BOOL, default=False,
        description="是否允许防御其他公会玩家",
    ),
    ConfigItem(
        key="bInvisibleOtherGuildBaseCampAreaFX", label_cn="隐藏其他公会基地特效", group="可见性",
        config_type=ConfigType.BOOL, default=False,
        description="是否隐藏其他公会基地范围的特效显示",
    ),
    ConfigItem(
        key="bBuildAreaLimit", label_cn="启用建造区域限制", group="可见性",
        config_type=ConfigType.BOOL, default=False,
        description="是否限制建造区域范围",
    ),

    # ==================== 物品重量 ====================
    ConfigItem(
        key="ItemWeightRate", label_cn="物品重量倍率", group="物品重量",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="所有物品重量的倍率",
    ),

    # ==================== 玩家数量 ====================
    ConfigItem(
        key="CoopPlayerMaxNum", label_cn="合作模式最大玩家数", group="玩家数量",
        config_type=ConfigType.INT, default=4,
        min_val=1, max_val=256, step=1,
        description="合作模式下最大玩家数量",
    ),
    ConfigItem(
        key="ServerPlayerMaxNum", label_cn="服务器最大玩家数", group="玩家数量",
        config_type=ConfigType.INT, default=32,
        min_val=1, max_val=256, step=1,
        description="服务器允许的最大玩家同时在线数",
    ),

    # ==================== 服务器信息 ====================
    ConfigItem(
        key="ServerName", label_cn="服务器名称", group="服务器信息",
        config_type=ConfigType.STRING, default="Default Palworld Server",
        description="服务器名称",
    ),
    ConfigItem(
        key="ServerDescription", label_cn="服务器描述", group="服务器信息",
        config_type=ConfigType.STRING, default="",
        description="服务器的简要描述",
    ),
    ConfigItem(
        key="AdminPassword", label_cn="管理员密码", group="服务器信息",
        config_type=ConfigType.STRING, default="",
        password=True,
        description="服务器管理员登录密码",
    ),
    ConfigItem(
        key="ServerPassword", label_cn="服务器密码", group="服务器信息",
        config_type=ConfigType.STRING, default="",
        password=True,
        description="玩家加入服务器所需密码",
    ),
    ConfigItem(
        key="bAllowClientMod", label_cn="允许客户端Mod", group="服务器信息",
        config_type=ConfigType.BOOL, default=True,
        description="是否允许客户端使用Mod",
    ),

    # ==================== 网络端口 ====================
    ConfigItem(
        key="PublicPort", label_cn="公开端口", group="网络端口",
        config_type=ConfigType.INT, default=8211,
        min_val=1, max_val=65535, step=1,
        description="服务器公开端口号",
    ),
    ConfigItem(
        key="QueryPort", label_cn="查询端口", group="网络端口",
        config_type=ConfigType.INT, default=27016,
        min_val=1, max_val=65535, step=1,
        description="Steam 服务器浏览器查询端口号",
    ),
    ConfigItem(
        key="PublicIP", label_cn="公开IP地址", group="网络端口",
        config_type=ConfigType.STRING, default="",
        description="服务器公开IP地址",
    ),

    # ==================== RCON（远程控制） ====================
    ConfigItem(
        key="RCONEnabled", label_cn="启用RCON", group="RCON（远程控制）",
        config_type=ConfigType.BOOL, default=False,
        description="是否启用远程控制（RCON）",
    ),
    ConfigItem(
        key="RCONPort", label_cn="RCON端口", group="RCON（远程控制）",
        config_type=ConfigType.INT, default=25575,
        min_val=1, max_val=65535, step=1,
        description="RCON 远程控制端口号",
    ),

    # ==================== 地区与认证 ====================
    ConfigItem(
        key="Region", label_cn="地区", group="地区与认证",
        config_type=ConfigType.STRING, default="",
        description="服务器所在地区",
    ),
    ConfigItem(
        key="bUseAuth", label_cn="使用认证", group="地区与认证",
        config_type=ConfigType.BOOL, default=True,
        description="是否使用身份认证系统",
    ),

    # ==================== 封禁列表 ====================
    ConfigItem(
        key="BanListURL", label_cn="封禁列表URL", group="封禁列表",
        config_type=ConfigType.STRING,
        default="https://b.palworldgame.com/api/banlist.txt",
        description="封禁玩家列表的URL地址",
    ),

    # ==================== REST API ====================
    ConfigItem(
        key="RESTAPIEnabled", label_cn="启用REST API", group="REST API",
        config_type=ConfigType.BOOL, default=False,
        description="是否启用REST API接口",
    ),
    ConfigItem(
        key="RESTAPIPort", label_cn="REST API端口", group="REST API",
        config_type=ConfigType.INT, default=8212,
        min_val=1, max_val=65535, step=1,
        description="REST API端口号",
    ),

    # ==================== 聊天与其他 ====================
    ConfigItem(
        key="bShowPlayerList", label_cn="显示玩家列表", group="聊天与其他",
        config_type=ConfigType.BOOL, default=False,
        description="是否在服务器中显示玩家列表",
    ),
    ConfigItem(
        key="ChatPostLimitPerMinute", label_cn="每分钟聊天限制", group="聊天与其他",
        config_type=ConfigType.INT, default=30,
        min_val=0, max_val=1000, step=1,
        description="玩家每分钟最大发送聊天消息数",
    ),
    ConfigItem(
        key="CrossplayPlatforms", label_cn="跨平台支持", group="聊天与其他",
        config_type=ConfigType.STRING, default="(Steam,Xbox,PS5,Mac)",
        description="支持的跨平台列表（格式: (Steam,Xbox,PS5,Mac)）",
    ),
    ConfigItem(
        key="bIsUseBackupSaveData", label_cn="使用备份存档", group="聊天与其他",
        config_type=ConfigType.BOOL, default=True,
        description="是否启用备份存档数据",
    ),
    ConfigItem(
        key="LogFormatType", label_cn="日志格式类型", group="聊天与其他",
        config_type=ConfigType.ENUM, default="Text",
        options=["Text", "Json"],
        description="日志输出格式类型",
    ),
    ConfigItem(
        key="bIsShowJoinLeftMessage", label_cn="显示加入/离开消息", group="聊天与其他",
        config_type=ConfigType.BOOL, default=True,
        description="是否在聊天中显示玩家加入/离开消息",
    ),

    # ==================== 补给与事件 ====================
    ConfigItem(
        key="SupplyDropSpan", label_cn="补给空投间隔（秒）", group="补给与事件",
        config_type=ConfigType.INT, default=180,
        min_val=0, max_val=7200, step=10,
        description="补给空投事件间隔时间（0=禁用）",
    ),
    ConfigItem(
        key="EnablePredatorBossPal", label_cn="启用捕食者首领帕鲁", group="补给与事件",
        config_type=ConfigType.BOOL, default=True,
        description="是否启用捕食者首领帕鲁事件",
    ),

    # ==================== 建筑限制 ====================
    ConfigItem(
        key="MaxBuildingLimitNum", label_cn="最大建筑数量限制", group="建筑限制",
        config_type=ConfigType.INT, default=0,
        min_val=0, max_val=100000, step=100,
        description="服务器最大建筑数量（0=无限制）",
    ),

    # ==================== 服务器性能 ====================
    ConfigItem(
        key="ServerReplicatePawnCullDistance", label_cn="角色复制剔除距离", group="服务器性能",
        config_type=ConfigType.FLOAT, default=15000.0,
        min_val=1000.0, max_val=100000.0, step=1000.0, decimals=6,
        description="服务器复制角色时的剔除距离",
    ),

    # ==================== 帕鲁箱导入/导出 ====================
    ConfigItem(
        key="bAllowGlobalPalboxExport", label_cn="允许全局帕鲁箱导出", group="帕鲁箱导入/导出",
        config_type=ConfigType.BOOL, default=True,
        description="是否允许从全局帕鲁箱导出帕鲁",
    ),
    ConfigItem(
        key="bAllowGlobalPalboxImport", label_cn="允许全局帕鲁箱导入", group="帕鲁箱导入/导出",
        config_type=ConfigType.BOOL, default=False,
        description="是否允许向全局帕鲁箱导入帕鲁",
    ),

    # ==================== 装备耐久 ====================
    ConfigItem(
        key="EquipmentDurabilityDamageRate", label_cn="装备耐久消耗倍率", group="装备耐久",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="装备耐久度消耗速度倍率",
    ),

    # ==================== 性能/同步 ====================
    ConfigItem(
        key="ItemContainerForceMarkDirtyInterval", label_cn="物品容器脏标记间隔", group="性能/同步",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.1, max_val=60.0, step=0.1, decimals=6,
        description="物品容器强制标记脏数据的时间间隔",
    ),
    ConfigItem(
        key="PlayerDataPalStorageUpdateCheckTickInterval", label_cn="帕鲁存储更新检查间隔", group="性能/同步",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.1, max_val=60.0, step=0.1, decimals=6,
        description="玩家帕鲁存储更新检查间隔",
    ),

    # ==================== 物品腐败 ====================
    ConfigItem(
        key="ItemCorruptionMultiplier", label_cn="物品腐败倍率", group="物品腐败",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="物品腐败速度倍率",
    ),

    # ==================== 帕鲁农场 ====================
    ConfigItem(
        key="MonsterFarmActionSpeedRate", label_cn="帕鲁农场动作速度倍率", group="帕鲁农场",
        config_type=ConfigType.FLOAT, default=1.0,
        min_val=0.0, max_val=10.0, step=0.1, decimals=6,
        description="帕鲁在农场的动作速度倍率",
    ),

    # ==================== 科技限制 ====================
    ConfigItem(
        key="DenyTechnologyList", label_cn="禁止科技列表", group="科技限制",
        config_type=ConfigType.STRING, default="",
        description="禁止研究的科技列表（逗号分隔）",
    ),

    # ==================== 公会重新加入 ====================
    ConfigItem(
        key="GuildRejoinCooldownMinutes", label_cn="公会重新加入冷却（分钟）", group="公会重新加入",
        config_type=ConfigType.INT, default=0,
        min_val=0, max_val=10080, step=1,
        description="离开公会后重新加入的冷却时间（分钟）",
    ),

    # ==================== 自动转移主人 ====================
    ConfigItem(
        key="AutoTransferMasterCheckIntervalSeconds", label_cn="自动转移主人检查间隔", group="自动转移主人",
        config_type=ConfigType.FLOAT, default=3600.0,
        min_val=60.0, max_val=86400.0, step=60.0, decimals=6,
        description="自动转移主人检查间隔（秒）",
    ),
    ConfigItem(
        key="AutoTransferMasterThresholdDays", label_cn="自动转移主人阈值（天）", group="自动转移主人",
        config_type=ConfigType.INT, default=14,
        min_val=1, max_val=365, step=1,
        description="玩家离线多少天后触发自动转移主人",
    ),

    # ==================== 性能 ====================
    ConfigItem(
        key="MaxGuildsPerFrame", label_cn="每帧最大公会处理数", group="性能",
        config_type=ConfigType.INT, default=10,
        min_val=1, max_val=1000, step=1,
        description="每帧最大处理的公会数量",
    ),

    # ==================== 重生 ====================
    ConfigItem(
        key="BlockRespawnTime", label_cn="重生阻挡时间", group="重生",
        config_type=ConfigType.FLOAT, default=5.0,
        min_val=0.0, max_val=60.0, step=1.0, decimals=6,
        description="重生被阻挡时需要等待的时间",
    ),
    ConfigItem(
        key="RespawnPenaltyDurationThreshold", label_cn="重生惩罚持续时间阈值", group="重生",
        config_type=ConfigType.FLOAT, default=0.0,
        min_val=0.0, max_val=3600.0, step=1.0, decimals=6,
        description="触发重生惩罚的持续时间阈值",
    ),
    ConfigItem(
        key="RespawnPenaltyTimeScale", label_cn="重生惩罚时间比例", group="重生",
        config_type=ConfigType.FLOAT, default=2.0,
        min_val=1.0, max_val=10.0, step=0.5, decimals=6,
        description="重生惩罚的时间比例",
    ),

    # ==================== PvP显示 ====================
    ConfigItem(
        key="bDisplayPvPItemNumOnWorldMap_BaseCamp", label_cn="世界地图显示基地PvP物品数", group="PvP显示",
        config_type=ConfigType.BOOL, default=False,
        description="是否在世界地图上显示基地PvP物品数量",
    ),
    ConfigItem(
        key="bDisplayPvPItemNumOnWorldMap_Player", label_cn="世界地图显示玩家PvP物品数", group="PvP显示",
        config_type=ConfigType.BOOL, default=False,
        description="是否在世界地图上显示玩家PvP物品数量",
    ),

    # ==================== PvP额外掉落 ====================
    ConfigItem(
        key="AdditionalDropItemWhenPlayerKillingInPvPMode", label_cn="PvP击杀额外掉落类型", group="PvP额外掉落",
        config_type=ConfigType.STRING, default="PlayerDropItem",
        description="PvP击杀时额外掉落的物品类型",
    ),
    ConfigItem(
        key="AdditionalDropItemNumWhenPlayerKillingInPvPMode", label_cn="PvP击杀额外掉落数量", group="PvP额外掉落",
        config_type=ConfigType.INT, default=1,
        min_val=0, max_val=100, step=1,
        description="PvP击杀时额外掉落的物品数量",
    ),
    ConfigItem(
        key="bAdditionalDropItemWhenPlayerKillingInPvPMode", label_cn="启用PvP击杀额外掉落", group="PvP额外掉落",
        config_type=ConfigType.BOOL, default=False,
        description="是否在PvP击杀时启用额外物品掉落",
    ),

    # ==================== 语音聊天 ====================
    ConfigItem(
        key="bEnableVoiceChat", label_cn="启用语音聊天", group="语音聊天",
        config_type=ConfigType.BOOL, default=False,
        description="是否启用服务器语音聊天",
    ),
    ConfigItem(
        key="VoiceChatMaxVolumeDistance", label_cn="语音聊天最大音量距离", group="语音聊天",
        config_type=ConfigType.FLOAT, default=3000.0,
        min_val=100.0, max_val=50000.0, step=100.0, decimals=6,
        description="语音聊天最大音量可听距离",
    ),
    ConfigItem(
        key="VoiceChatZeroVolumeDistance", label_cn="语音聊天音量归零距离", group="语音聊天",
        config_type=ConfigType.FLOAT, default=15000.0,
        min_val=100.0, max_val=100000.0, step=100.0, decimals=6,
        description="语音聊天音量降至零的距离",
    ),

    # ==================== 属性强化 ====================
    ConfigItem(
        key="bAllowEnhanceStat_Health", label_cn="允许提升生命值", group="属性强化",
        config_type=ConfigType.BOOL, default=True,
        description="是否允许玩家提升生命值属性",
    ),
    ConfigItem(
        key="bAllowEnhanceStat_Attack", label_cn="允许提升攻击力", group="属性强化",
        config_type=ConfigType.BOOL, default=True,
        description="是否允许玩家提升攻击力属性",
    ),
    ConfigItem(
        key="bAllowEnhanceStat_Stamina", label_cn="允许提升体力", group="属性强化",
        config_type=ConfigType.BOOL, default=True,
        description="是否允许玩家提升体力属性",
    ),
    ConfigItem(
        key="bAllowEnhanceStat_Weight", label_cn="允许提升负重", group="属性强化",
        config_type=ConfigType.BOOL, default=True,
        description="是否允许玩家提升负重属性",
    ),
    ConfigItem(
        key="bAllowEnhanceStat_WorkSpeed", label_cn="允许提升工作速度", group="属性强化",
        config_type=ConfigType.BOOL, default=True,
        description="是否允许玩家提升工作速度属性",
    ),

    # ==================== 建筑显示 ====================
    ConfigItem(
        key="bEnableBuildingPlayerUIdDisplay", label_cn="显示建筑玩家UID", group="建筑显示",
        config_type=ConfigType.BOOL, default=False,
        description="是否在建筑上显示建造玩家的UID",
    ),
    ConfigItem(
        key="BuildingNameDisplayCacheTTLSeconds", label_cn="建筑名称显示缓存TTL", group="建筑显示",
        config_type=ConfigType.INT, default=60,
        min_val=1, max_val=3600, step=1,
        description="建筑名称显示缓存的生存时间（秒）",
    ),
]


def get_defaults() -> dict[str, Any]:
    """返回所有配置项的默认值字典"""
    return {item.key: item.default for item in CONFIG_SCHEMA}


def get_item(key: str) -> ConfigItem | None:
    """根据 key 查找配置项"""
    for item in CONFIG_SCHEMA:
        if item.key == key:
            return item
    return None


def get_groups() -> list[str]:
    """返回有序的分组列表"""
    seen = []
    for item in CONFIG_SCHEMA:
        if item.group not in seen:
            seen.append(item.group)
    return seen
