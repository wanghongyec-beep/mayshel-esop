#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MES 操作指导书 HTML 生成器 v3
- 8 模块完整内容
- 层级子步骤 (1.1, 1.2, ...)
- 图文配对布局
- 作业说明 + 备注
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# 内容定义（结构化，不再从 Word 解析）
# ============================================================
# 每张图片说明：{img: 文件名, desc: 图注}
# 每个子步骤：{id, name, desc(作业说明), remark(备注), images: [{img, desc}]}

CONTENT = {
    "injection": {
        "title": "注塑车间操作手册",
        "dept": "生产部",
        "icon": "🏭",
        "img_dir": "images/production-injection",
        "scenario": [
            "注塑车间通过 MES 系统实现从派工到报工的全流程数字化管理。班组长根据生产计划在系统中进行派工作业，将工单精准分配至对应注塑机台；作业人员登录工作平台选择负责机台上工，并进行设备点检确保生产条件就绪；生产过程中执行进站/出站报工，完整记录生产数量和工时数据。",
            "本手册按「派工 → 上工 → 点检 → 报工」四大环节，详细说明每个操作步骤及系统截图对照。"
        ],
        "steps": [
            {
                "title": "1. 派工作业",
                "sub_steps": [
                    {
                        "id": "1.1", "name": "进入派工作业界面",
                        "desc": "登录 MES 系统后，在功能菜单中选择【派工作业】模块，进入派工管理主界面。系统默认显示当前未派工的生产批列表。",
                        "remark": "派工菜单权限由后端角色权限控制，如未看到派工菜单请联系管理员配置。",
                        "images": [{"img": "fig-01.png", "desc": "派工作业入口"}]
                    },
                    {
                        "id": "1.2", "name": "选择加工中心",
                        "desc": "在派工界面中，筛选需要派工的加工中心（如「注塑车间」），系统将展示该中心下所有待派工的生产批。支持按工单号、料号、日期等条件快速筛选。",
                        "remark": "加工中心在系统基础数据中配置，如列表为空请联系后端维护。",
                        "images": [{"img": "fig-02.png", "desc": "筛选加工中心"}]
                    },
                    {
                        "id": "1.3", "name": "检查齐套",
                        "desc": "选中生产批后，点击「齐套检查」按钮，系统自动校验物料、模具、工艺参数等是否齐套。齐套通过的生产批方可进行派工。",
                        "remark": "齐套检查的校验规则在后端「齐套参数设置」中配置。",
                        "images": [{"img": "fig-03.png", "desc": "齐套检查结果"}]
                    },
                    {
                        "id": "1.4", "name": "一键派工",
                        "desc": "齐套通过后，选中生产批点击「一键派工」，系统自动将工单分配至最优机台。也可手动选择目标机台后点击「派工」完成派工操作。派工成功后，该工单状态更新为「已派工」。",
                        "remark": "派工后会将用模信息抛转WMS，AGV送模。",
                        "images": [{"img": "fig-04.png", "desc": "一键派工完成"}]
                    }
                ]
            },
            {
                "title": "2. 上工作业",
                "sub_steps": [
                    {
                        "id": "2.1", "name": "进入产线平台",
                        "desc": "进入作业人员工作平台，系统显示当前登录人有权限的所有机台/产线。点击需要上工的机台旁的❤图标，将该机台加入「我的机台」列表，方便后续快速定位和操作。",
                        "remark": "如列表为空，请联系管理员配置账号的产线权限。",
                        "images": [
                            {"img": "fig-07.png", "desc": "产线平台概览"},
                            {"img": "fig-08.png", "desc": "加入我的机台"}
                        ]
                    },
                    {
                        "id": "2.2", "name": "选择报工群组",
                        "desc": "在平台中选择【报工群组】页签，系统展示当前负责的所有机台/产线。选择目标机台确认后完成上工，平台上工图标变为绿色表示上工成功。",
                        "remark": "报工群组需要在后端「报工群组设置」中提前维护。",
                        "images": [
                            {"img": "fig-07.png", "desc": "报工群组选择"}
                        ]
                    },
                    {
                        "id": "2.3", "name": "多人报同作业站",
                        "desc": "当一台设备需要多人同时作业时，支持多人上工至同一作业站。第二名及以上的作业人员直接点击该机台的【上工】按钮，系统允许同站多人在线。平台上工图标变为绿色表示上工成功。",
                        "remark": "多人报同站时，每人分别进行报工，产量分别记录。上工后方可进行报工操作，未上工不允许进站报工。",
                        "images": [{"img": "fig-09.png", "desc": "多人上工状态"}]
                    }
                ]
            },
            {
                "title": "3. 产线点检",
                "sub_steps": [
                    {
                        "id": "3.1", "name": "执行设备点检",
                        "desc": "在作业区工作平台选择已上工的机台，点击【点检】按钮。系统弹出点检窗体，按设备类型自动带出对应点检项目（如温度、压力、安全装置等），逐一填写点检值后点击确定完成点检。",
                        "remark": "可设置点检必须通过才允许进站报工。点检项目在后端「设备点检标准」中配置。点检未完成或点检结果为 NG 时，不允许进站报工（取决于后端参数设置）。",
                        "images": [
                            {"img": "fig-05.png", "desc": "点检项目填写"},
                            {"img": "fig-06.png", "desc": "点检完成确认"}
                        ]
                    }
                ]
            },
            {
                "title": "4. 报工作业",
                "sub_steps": [
                    {
                        "id": "4.1", "name": "上模作业",
                        "desc": "完成设备点检后，在作业平台选择对应机台，点击【上模】按钮。扫描或输入模具编号，系统校验模具与当前工单是否匹配。确认上模后模具信息自动更新，即可开始生产。",
                        "remark": "上模操作前需确保设备已完成点检且结果合格。",
                        "images": [
                            {"img": "fig-14.png", "desc": "上模操作入口"},
                            {"img": "fig-15.png", "desc": "上模界面"}
                        ]
                    },
                    {
                        "id": "4.2", "name": "进站报工",
                        "desc": "完成设备点检并上工后，在作业平台选择对应机台，点击【进站报工】。系统弹出报工界面，自动填入当前工单信息。输入本次进站生产的数量（批量数），确认后完成进站，代表本工序开始生产。",
                        "remark": "若需要打印袋标，则进站后会调取打印服务，打印袋标标签。",
                        "images": [
                            {"img": "fig-10.png", "desc": "进站报工入口"},
                            {"img": "fig-11.png", "desc": "进站数量录入"}
                        ]
                    },
                    {
                        "id": "4.3", "name": "查看工艺标准",
                        "desc": "此处获取PLM下发的注塑工艺标准，查看工艺标准，若确认无误，则点击下发按钮下发到机台。",
                        "remark": "注塑机需为手动模式才可下发。",
                        "images": [
                            {"img": "fig-12.png", "desc": "工艺标准查看"},
                            {"img": "fig-16.png", "desc": "工艺标准下发"}
                        ]
                    },
                    {
                        "id": "4.4", "name": "记录工艺参数",
                        "desc": "此处获取注塑机上的标准工艺参数，可查看整版工艺参数。点击上传PLM按钮，则可以将参数上传至PLM。",
                        "remark": "",
                        "images": [
                            {"img": "fig-13.png", "desc": "工艺参数记录"},
                            {"img": "fig-17.png", "desc": "整版工艺参数"}
                        ]
                    },
                    {
                        "id": "4.5", "name": "出站报工",
                        "desc": "手动出站报工：本工序生产完成后，点击需要出站的工单，选择【出站报工】。确认后完成出站，代表本工序完工。\n自动出站报工：MES会获取注塑机产量，达到托盘数量后执行自动报工。（当前均为自动报工）",
                        "remark": "出站报工后工序状态变更为「已完工」。出站时必须填写合格品数和不良品数，不良品数超过设定比例将触发异常流程，自动开立异常单。",
                        "images": [
                            {"img": "fig-11.png", "desc": "出站报工"}
                        ]
                    }
                ]
            }
        ],
        "notes": [
            "所有操作均需在当班次内完成，跨班次需要重新上工。"
        ]
    },
    "assembly": {
        "title": "组装车间操作手册",
        "dept": "生产部",
        "icon": "🏭",
        "img_dir": "images/production-assembly",
        "scenario": [
            "组装车间通过 MES 系统实现产线派工、人员上工、设备点检及进出站报工的数字化管理。班组长根据生产计划在系统中进行派工作业，将装配工单分配至对应产线；作业人员刷卡或扫码上工，完成产线点检后执行进站/出站报工。",
            "本手册详细说明组装车间各操作环节的系统操作步骤及截图对照。"
        ],
        "steps": [
            {
                "title": "1. 派工作业",
                "sub_steps": [
                    {
                        "id": "1.1", "name": "进入派工作业界面",
                        "desc": "登录 MES 系统后，在功能菜单中选择【派工作业】模块，进入派工管理主界面。系统默认显示当前未派工的生产批列表。",
                        "remark": "派工菜单权限由后端角色权限控制，如未看到派工菜单请联系管理员配置。",
                        "images": [{"img": "fig-01.png", "desc": "派工作业入口"}]
                    },
                    {
                        "id": "1.2", "name": "选择加工中心",
                        "desc": "在派工界面中，筛选需要派工的加工中心（如「组装车间」），系统将展示该中心下所有待派工的生产批。支持按工单号、料号、日期等条件快速筛选。",
                        "remark": "加工中心在系统基础数据中配置，如列表为空请联系后端维护。",
                        "images": [{"img": "fig-02.png", "desc": "筛选加工中心"}]
                    },
                    {
                        "id": "1.3", "name": "检查齐套",
                        "desc": "选中生产批后，点击「齐套检查」按钮，系统自动校验物料、模具、工艺参数等是否齐套。齐套通过的生产批方可进行派工。",
                        "remark": "齐套检查的校验规则在后端「齐套参数设置」中配置。",
                        "images": [{"img": "fig-03.png", "desc": "齐套检查结果"}]
                    },
                    {
                        "id": "1.4", "name": "一键派工",
                        "desc": "齐套通过后，选中生产批点击「一键派工」，系统自动将工单分配至最优机台。也可手动选择目标机台后点击「派工」完成派工操作。派工成功后，该工单状态更新为「已派工」。",
                        "remark": "派工后会将用模信息抛转WMS，AGV送模。",
                        "images": [{"img": "fig-04.png", "desc": "一键派工完成"}]
                    }
                ]
            },
            {
                "title": "2. 上工作业",
                "sub_steps": [
                    {
                        "id": "2.1", "name": "进入产线平台",
                        "desc": "进入作业人员工作平台，系统显示当前登录人有权限的所有机台/产线。点击需要上工的机台旁的❤图标，将该机台加入「我的机台」列表，方便后续快速定位和操作。",
                        "remark": "如列表为空，请联系管理员配置账号的产线权限。",
                        "images": [
                            {"img": "fig-05.png", "desc": "产线平台概览"}
                        ]
                    },
                    {
                        "id": "2.2", "name": "选择报工群组",
                        "desc": "在平台中选择【报工群组】页签，系统展示当前负责的所有机台/产线。选择目标机台确认后完成上工，平台上工图标变为绿色表示上工成功。",
                        "remark": "报工群组需要在后端「报工群组设置」中提前维护。",
                        "images": [
                            {"img": "fig-19.png", "desc": "报工群组选择"}
                        ]
                    },
                    {
                        "id": "2.3", "name": "多人报同作业站",
                        "desc": "当一台设备需要多人同时作业时，支持多人上工至同一作业站。第二名及以上的作业人员直接点击该机台的【上工】按钮，系统允许同站多人在线。平台上工图标变为绿色表示上工成功。",
                        "remark": "多人报同站时，每人分别进行报工，产量分别记录。上工后方可进行报工操作，未上工不允许进站报工。",
                        "images": [{"img": "fig-18.png", "desc": "多人上工状态"}]
                    }
                ]
            },
            {
                "title": "3. 产线点检",
                "sub_steps": [
                    {
                        "id": "3.1", "name": "执行设备点检",
                        "desc": "在作业区工作平台选择已上工的机台，点击【点检】按钮。系统弹出点检窗体，按设备类型自动带出对应点检项目（如温度、压力、安全装置等），逐一填写点检值后点击确定完成点检。",
                        "remark": "可设置点检必须通过才允许进站报工。点检项目在后端「设备点检标准」中配置。点检未完成或点检结果为 NG 时，不允许进站报工（取决于后端参数设置）。",
                        "images": [
                            {"img": "fig-07.png", "desc": "点检入口"},
                            {"img": "fig-08.png", "desc": "点检项目填写"}
                        ]
                    }
                ]
            },
            {
                "title": "4. 报工作业",
                "sub_steps": [
                    {
                        "id": "4.1", "name": "进站报工",
                        "desc": "点检完成后，在作业平台选择对应产线/设备，点击【进站报工】。进入报工界面后，填入本次进站的生产数量，确认后完成进站报工。进站后该工单状态变为「生产中」。",
                        "remark": "",
                        "images": [
                            {"img": "fig-09.png", "desc": "进站报工入口"},
                            {"img": "fig-10.png", "desc": "进站数量录入"}
                        ]
                    },
                    {
                        "id": "4.2", "name": "出站报工",
                        "desc": "组装出站由线尾的照相机扫码出站，装箱人员需提前将箱码粘贴到外箱。照相机扫码后，会执行自动出站，无需人工干预。",
                        "remark": "出站数量达到产品对应的检验数后，会生成下一张检验单。",
                        "images": []
                    }
                ]
            }
        ],
        "notes": []
    },
    "equipment": {
        "title": "设备维保操作手册",
        "dept": "设备部",
        "icon": "⚙️",
        "img_dir": "images/equipment",
        "scenario": [
            "设备稼动是 MES 系统中对设备状态进行管理的核心功能。设备发生状态转换（设置→加工中→故障→维修→保养→暂停→关机等）时，通过选择设备进行设备稼动操作，切换目标状态并记录原因，实现设备全生命周期状态追溯与闭环管理。",
            "设备稼动操作入口包括：作业人员工作平台、生产管理工作平台、生产线管控平台。设备共有八个稼动状态：设置、加工中、故障、维修、保养、暂停、设置、关机。",
            "本手册覆盖设备稼动状态变更操作（含完整闭环流程）及设备保养作业的系统操作步骤。",
            "参考文档：PL102 设备稼动管理操作简报"
        ],
        "steps": [
            {
                "title": "1. 设备稼动",
                "sub_steps": [
                    {
                        "id": "1.1", "name": "进入工作平台",
                        "desc": "登录 MES 系统后，进入【作业人员工作平台】（或生产管理工作平台/生产线管控平台），查看当前所有设备的实时状态。设备状态以不同颜色标识：加工中（绿色/蓝色）、故障（红色）、维修（橙色）、保养（黄色）、暂停（紫色）、设置/关机（灰色）等。",
                        "remark": "工作平台权限由后端角色权限控制，如未看到对应菜单请联系管理员配置。",
                        "images": [{"img": "fig-01.png", "desc": "工作平台设备状态总览"}]
                    },
                    {
                        "id": "1.2", "name": "选择设备并执行稼动",
                        "desc": "选择需要进行稼动操作的设备，点击【设备稼动】按钮，弹出稼动操作窗口。在稼动窗口中先勾选要稼动的目标状态（如故障、维修、保养、暂停、设置、关机），然后根据目标状态选择对应的稼动原因。确认后设备状态即时变更并留档记录。",
                        "remark": "稼动类型与原因在后端【设备状态原因基础资料】中配置。故障、维修、保养、暂停等状态需要选择稼动原因（必选项）；关机、加工中状态可不用选择原因。设备故障状态切换可结合安灯按板预报警（PL207）；设备维修状态切换通过设备报修（PL201）。",
                        "images": [
                            {"img": "fig-02.png", "desc": "设备稼动操作窗口"},
                            {"img": "fig-03.png", "desc": "稼动状态与原因选择"}
                        ]
                    },
                    {
                        "id": "1.3", "name": "确认稼动结果",
                        "desc": "设备稼动成功后，设备状态即时变更并显示对应颜色。例如选择稼动类别=故障，则设备状态变更为故障（红色），同时系统记录该设备的状态变更时间、操作人、变更原因等信息，形成设备状态履历。",
                        "remark": "设备状态变更后的结果可在【设备稼动历程日报表】中按日查询每台设备的稼动历程。",
                        "images": [{"img": "fig-04.png", "desc": "设备稼动成功状态变更"}]
                    },
                    {
                        "id": "1.4", "name": "设备稼动闭环流程",
                        "desc": "设备稼动的核心原则是「闭环」：原状态→目标状态→回归原状态。以设备维修为例，完整闭环流程为：加工中→故障（发生故障）→维修（维修中）→加工中（维修完成恢复生产）。同理，保养、暂停、设置等状态变更均遵循此闭环原则。",
                        "remark": "设备在故障、维修、保养、暂停、设置、关机状态期间，无法执行进站报工作业（产线管控平台除外）。设备若接入 IoT 采集，以采集数据为准更新稼动状态。",
                        "images": [
                            {"img": "fig-05.png", "desc": "维修状态稼动"},
                            {"img": "fig-06.png", "desc": "维修完成恢复加工中状态"}
                        ]
                    }
                ]
            },
            {
                "title": "2. 设备状态变更场景",
                "sub_steps": [
                    {
                        "id": "2.1", "name": "设备设置→加工中",
                        "desc": "每日上班时，操作人员在工作平台选择目标设备，点击【设备稼动】，将设备从「设置」状态切换为「加工中」状态。随后执行进站操作（Q状态→R状态），设备状态自动变为加工中（绿色），开始生产加工。",
                        "remark": "设备上开始生产作业前需执行进站操作，进站后设备自动切换为加工中状态；生产完成出站后设备自动切换回设置状态。",
                        "images": [
                            {"img": "fig-07.png", "desc": "进站加工/切换至加工中"},
                            {"img": "fig-08.png", "desc": "设备设置状态"}
                        ]
                    },
                    {
                        "id": "2.2", "name": "加工中→故障→维修→加工中（维修闭环）",
                        "desc": "生产过程中设备发生故障时，操作人员选择设备执行稼动，将状态从「加工中」切换为「故障」（选择故障原因）。维修人员到达后，将状态从「故障」切换为「维修」（选择维修原因并预计处理时间）。维修完成后，将状态切回「加工中」（填写实际维修时间），完成维修闭环。",
                        "remark": "维修状态切换必须经由「故障」状态，不能直接从加工中切换为维修。维修完成只能切换回故障前的状态。故障/维修原因在【设备-原因设定】中绑定。",
                        "images": [
                            {"img": "fig-09.png", "desc": "设备故障状态切换"},
                            {"img": "fig-10.png", "desc": "恢复加工中状态"}
                        ]
                    },
                    {
                        "id": "2.3", "name": "加工中→保养→加工中（保养闭环）",
                        "desc": "当设备到达保养计划时间或需要临时保养时，操作人员选择设备执行稼动，将状态从「加工中」切换为「保养」（选择保养原因并预计保养时长）。保养完成后切回「加工中」，完成保养闭环。若有保养单据，可在保养界面点击蓝色保养单入口查看保养项目和备品备件清单。",
                        "remark": "若设备当天存在已下发的保养单据，设备稼动为保养状态时会显示蓝色保养单入口。保养完成后设备需通过稼动回到加工中状态。保养计划在后端【设备保养计划】中设定。",
                        "images": [
                            {"img": "fig-11.png", "desc": "设备保养状态"},
                            {"img": "fig-12.png", "desc": "保养完成恢复加工中"}
                        ]
                    },
                    {
                        "id": "2.4", "name": "加工中→暂停/关机→加工中",
                        "desc": "休息时间或换班时，可将设备从「加工中」切换为「暂停」（选择暂停原因并预计暂停时长），休息结束后切回「加工中」。下班时切换为「关机」状态，次日上班再切回「设置」或「加工中」。",
                        "remark": "暂停原因是可选非必填项。关机状态下无法执行生产作业。设备在每个班次结束后建议切换为关机状态，以准确记录设备稼动率。",
                        "images": [
                            {"img": "fig-13.png", "desc": "设备暂停状态"},
                            {"img": "fig-14.png", "desc": "设备关机状态"}
                        ]
                    }
                ]
            },
            {
                "title": "3. 设备保养作业",
                "sub_steps": [
                    {
                        "id": "3.1", "name": "保养计划设定与下达",
                        "desc": "设备管理员在 MES 后端【设备管理】→【设备保养计划】功能中设定保养计划。选择需要保养的设备，设定保养周期（按日历时间：每月/每季度；或按运行时长触发），指定保养项目和备品备件清单。保养计划设定并签核后，系统按计划自动下发保养单据到对应设备。当设备到达保养日期时，操作人员在工作平台可看到设备显示待保养标志。",
                        "remark": "保养计划设定后，系统根据计划周期自动生成保养工单并推送至对应设备责任人。保养单据包含保养项目明细、使用备品、操作说明等信息。",
                        "images": [{"img": "fig-15.png", "desc": "设备保养原因设定/计划维护"}]
                    },
                    {
                        "id": "3.2", "name": "执行保养作业",
                        "desc": "当设备存在已下发的保养单据时，将设备稼动为「保养」状态后，系统显示蓝色保养单入口。点击进入保养单界面，查看本次保养的所有项目和所需备品备件。点击【开始保养】记录开始时间，逐项完成保养操作并填写保养结果，完成后点击【保养完毕】记录完成时间。保养记录自动更新到设备履历中。",
                        "remark": "保养完成后设备需通过稼动回到「加工中」状态。保养记录可在后续报表中追溯查询。",
                        "images": [
                            {"img": "fig-16.png", "desc": "设备保养设定/状态变更"}
                        ]
                    }
                ]
            }
        ],
        "notes": [
            "设备稼动为保养时，必须存在已下发的保养单据才可进行设备保养操作。",
            "设备在故障、维修、保养、暂停状态期间，在作业人员/生产管理工作平台上无法执行进站报工作业。",
            "设备状态变更遵循「原状态→目标状态→原状态」的闭环原则，维修完成/保养完成只能恢复至变更前的状态。",
            "设备稼动状态可安灯按板预报警（故障）或设备报修（维修）触发，详见 PL207/PL201 相关模块。"
        ]
    },
    "mold": {
        "title": "模具维保操作手册",
        "dept": "模具部",
        "icon": "🔧",
        "img_dir": "images/mold",
        "scenario": [
            "模具是注塑生产中的核心工艺装备，在 sMES 系统中对模具进行全生命周期管理：从模具基础资料建立、上下模作业、寿命管理，到异常叫修、维修执行、定期保养、异动管理及报表查询。",
            "本手册覆盖模具异常叫修、模具维修执行、模具定期保养及模具报表查看四大场景的系统操作，强调叫修→维修→完工确认的维修闭环以及保养计划→保养执行的保养闭环。",
            "参考文档：PL205 模治具寿命管理操作简报"
        ],
        "steps": [
            {
                "title": "1. 模具异常叫修",
                "sub_steps": [
                    {
                        "id": "1.1", "name": "异常叫修",
                        "desc": "生产过程中发现模具异常时，生产人员在设备工作平台执行异常下模操作，在【模具管理】→【模具维修管理】模块中点击【异常叫修】，系统弹出叫修界面。选择异常模具、填写异常现象（如模具损坏、产品毛边、顶针断裂等），确认后提交叫修单。异常单自动推送至模具部维修人员待办列表，模具状态变更为待维修。",
                        "remark": "异常叫修单包含模具编号、异常现象描述、发生时间、紧急程度等信息。异常类型可在后端配置。",
                        "images": [{"img": "fig-01.png", "desc": "模具异常叫修界面"}]
                    },
                    {
                        "id": "1.2", "name": "叫修单跟踪",
                        "desc": "提交叫修后，模具部维修人员在【模具维修管理】模块中可查看所有待处理的叫修单据。列表显示模具编号、异常描述、紧急程度、申请人、申请时间等信息。维修人员【签收】单据后，叫修单状态更新为处理中，同时通知申请人。",
                        "remark": "维修任务支持按紧急程度排序，紧急任务优先处理。",
                        "images": [{"img": "fig-02.png", "desc": "待维修模具列表/叫修单跟踪"}]
                    }
                ]
            },
            {
                "title": "2. 模具维修执行（维修闭环）",
                "sub_steps": [
                    {
                        "id": "2.1", "name": "执行维修作业",
                        "desc": "维修人员签收叫修单后，进入维修执行界面。查看异常详情和历史维修记录辅助故障判断。维修完成后在系统中填写维修结果：维修内容描述、更换配件明细（配件编号、名称、数量）、维修工时等。确认提交后，模具状态从维修中更新为可用/在库状态。",
                        "remark": "维修执行时可查看模具历史维修履历，辅助快速定位故障原因。维修记录自动保存至模具全生命周期履历中。",
                        "images": [{"img": "fig-03.png", "desc": "模具维修执行界面"}]
                    },
                    {
                        "id": "2.2", "name": "维修完工确认（闭环）",
                        "desc": "维修完成后，系统在模具履历中自动生成一条维修记录，包含：维修时间、维修人员、故障原因、维修内容、更换配件清单等。模具状态从维修中恢复为可用/在库状态，可重新上线使用。完整维修闭环：异常发现→叫修→签收→维修作业→完工确认→恢复可用。",
                        "remark": "维修记录可在【模具履历查询】和【维修记录报表】中追溯查询，支持按模具编号、时间段等条件筛选。",
                        "images": [{"img": "fig-04.png", "desc": "模具维修完工确认界面"}]
                    }
                ]
            },
            {
                "title": "3. 模具定期保养（保养闭环）",
                "sub_steps": [
                    {
                        "id": "3.1", "name": "维护保养计划",
                        "desc": "模具人员在【模具定期保养计划】功能中，根据模具类型和使用频率设定保养周期。支持按模次触发（如每10万模次保养一次）和按日历时间触发（如每月/每季度保养一次）。系统按计划自动生成保养任务并推送到对应责任人。保养计划包含保养项目明细和标准说明。",
                        "remark": "保养计划设定后，模具进站报工时系统会校验模具使用次数是否达到保养预警值并给出提示。",
                        "images": [{"img": "fig-05.png", "desc": "模具定期保养计划维护"}]
                    },
                    {
                        "id": "3.2", "name": "执行保养作业（闭环）",
                        "desc": "当保养任务到达执行日期或模次时，模具人员在【模具保养任务】中查看保养任务单。逐项完成保养项目（清洗、润滑、精度检测、易损件更换等），填写保养结果后提交。保养完成后模具状态更新为已保养，可继续上线生产。完整保养闭环：计划设定→任务生成→保养执行→完工确认→更新状态。",
                        "remark": "保养项目及标准可在后端【模具保养项目】中配置。保养记录自动更新至模具保养履历。",
                        "images": [{"img": "fig-06.png", "desc": "模具保养执行界面"}]
                    }
                ]
            },
            {
                "title": "4. 模具报表查看",
                "sub_steps": [
                    {
                        "id": "4.1", "name": "查看模具履历报表",
                        "desc": "在 MES 系统中可查看模具相关的各类报表：模具履历（全生命周期记录）、维修记录报表、保养记录报表、模具寿命预警报表、模具当前状态查询等。支持按模具编号、类型、日期等条件筛选查询。所有数据来源于日常操作记录，如实填写是报表准确性的基础。",
                        "remark": "模具报表数据帮助追溯模具全生命周期状态，为模具寿命管理和维保决策提供数据支撑。",
                        "images": [{"img": "fig-07.png", "desc": "模具履历报表查询"}]
                    }
                ]
            }
        ],
        "notes": [
            "模具全生命周期涵盖：基础资料建立→发放→上模→生产→下模→维修/保养→入库，形成完整闭环管理。",
            "维修闭环：异常发现→叫修→签收→维修作业→完工确认→恢复可用。",
            "保养闭环：计划设定→任务生成→保养执行→完工确认→状态更新。",
            "严格按计划执行模具保养，可有效延长模具使用寿命，降低维修成本。"
        ]
    },
    "quality": {
        "title": "质量检验操作手册",
        "dept": "质量部",
        "icon": "📋",
        "img_dir": "images/quality",
        "scenario": [
            "在生产流程中对半成品或关键工序进行动态监控。在 MES 中关键工序发起首检后生成 PQC 首件检查单据，进站后生成检验单据、出站后生成检验单据，供检验员进行检验及异常处理操作。",
            "注：IQC 检验前端检验作业流程与 PQC 一致，但单据发起由 ERP 进行操作。",
            "本手册说明 PQC 检验作业及质量异常处置两大模块的系统操作步骤。"
        ],
        "steps": [
            {
                "title": "1. PQC 检验作业",
                "sub_steps": [
                    {
                        "id": "1.1", "name": "进入检验清单",
                        "desc": "在质量检验模块中，进入【PQC 检验清单】页面。列表显示所有需要检验的单据，按状态分为「未确认」「未检验」「已验收」等页签。",
                        "remark": "",
                        "images": [
                            {"img": "fig-01.png", "desc": "质量检验模块"},
                            {"img": "fig-02.png", "desc": "检验清单界面"}
                        ]
                    },
                    {
                        "id": "1.2", "name": "未确认单据 → 确认",
                        "desc": "在「未确认」页签中，系统列出待确认的检验单据。选中需要操作的检验单，点击确认按钮，单据流转至「待检验」状态，等待检验员进行检验操作。",
                        "remark": "",
                        "images": [
                            {"img": "fig-03.png", "desc": "未确认页签"},
                            {"img": "fig-04.png", "desc": "确认操作"}
                        ]
                    },
                    {
                        "id": "1.3", "name": "计量检验项目录入",
                        "desc": "进入「待检验」页签，选中检验单后进入检验界面。选择【计量检验项目】页签，使用量具测量后将实际测量值填入系统对应项目输入框中。系统自动根据规格上下限判定合格/不合格（绿色为合格）。",
                        "remark": "计量项目超出规格自动开立异常单。检验值超过规格上限或低于下限时触发。",
                        "images": [
                            {"img": "fig-05.png", "desc": "选择计量检验项目"},
                            {"img": "fig-06.png", "desc": "计量值录入"}
                        ]
                    },
                    {
                        "id": "1.4", "name": "计数检验项目录入",
                        "desc": "切换至【计数检验项目】页签，根据实际检验情况选择各不良项目是否存在。若全部合格则不良数填 0；若存在不良则填入对应不良原因的数量。",
                        "remark": "计数项目按判别法则自动判定：当不良数达到设定标准时，系统自动开立异常单。",
                        "images": [
                            {"img": "fig-07.png", "desc": "计数检验项目"},
                            {"img": "fig-08.png", "desc": "不良原因选择"}
                        ]
                    },
                    {
                        "id": "1.5", "name": "异常单开立",
                        "desc": "当检验结果触发判别法则时（计量超差/计数不良超标/法则设定为异常），系统弹出异常单开立窗口。填入异常单的分类群组、第一处理群组、验收群组及不良原因，点击完成生成异常单。",
                        "remark": "满足以下条件之一即触发：1)计数不良达标准 2)计量超规格 3)法则设定为「异常」。",
                        "images": [
                            {"img": "fig-09.png", "desc": "异常单触发"},
                            {"img": "fig-10.png", "desc": "异常单填写"}
                        ]
                    },
                    {
                        "id": "1.6", "name": "判定检验结果",
                        "desc": "异常单开立完毕后回到判定界面。若存在异常单，判定时可选择：整批报废（损坏数量=母体数量，判定不合格）或部分允收。若未触发异常单，则正常判定全部合格：填入允收数量和损坏数量，完成判定。检验单流转至「已验收」页签。",
                        "remark": "",
                        "images": [
                            {"img": "fig-11.png", "desc": "判定界面"},
                            {"img": "fig-12.png", "desc": "判定完成"}
                        ]
                    }
                ]
            },
            {
                "title": "2. 质量异常处理",
                "sub_steps": [
                    {
                        "id": "2.1", "name": "查看异常单",
                        "desc": "进入 Web 端质量控制模块的【质量异常单】功能，查看系统自动生成的异常单据列表。各群组检验员仅看到自己负责的异常单。选中需要处理的异常单，点击编辑进入处置界面。",
                        "remark": "异常单每一步指派与处置结果判断都支持发送邮箱提醒。",
                        "images": [
                            {"img": "fig-13.png", "desc": "质量异常模块"},
                            {"img": "fig-14.png", "desc": "异常单列表"}
                        ]
                    },
                    {
                        "id": "2.2", "name": "第一群组新建处置记录",
                        "desc": "第一群组内的检验员在异常单界面新建处置记录，指派任意群组进行处理。填写处置说明后提交，异常单流转至被指派群组的待办列表。",
                        "remark": "",
                        "images": [
                            {"img": "fig-15.png", "desc": "新建处置记录"},
                            {"img": "fig-16.png", "desc": "指派群组"}
                        ]
                    },
                    {
                        "id": "2.3", "name": "被指派群组处置对策",
                        "desc": "被指派群组收到消息提醒后，进入【处置结果验证】界面。在处置对策中填写具体的处理措施和方案，判断本次处置结果为 OK 或 NG 后提交。",
                        "remark": "",
                        "images": [
                            {"img": "fig-17.png", "desc": "处置对策填写"},
                            {"img": "fig-18.png", "desc": "处置结果判定"}
                        ]
                    },
                    {
                        "id": "2.4", "name": "第一群组验证处置结果",
                        "desc": "第一群组收到处置完成通知后，对处置结果进行验证。输入验证耗时和验证说明。若验证结果 OK，则核准处置记录，异常单进入「结案中」状态；若 NG，则打回至被指派群组重新处理。",
                        "remark": "",
                        "images": [
                            {"img": "fig-19.png", "desc": "验证界面"},
                            {"img": "fig-20.png", "desc": "验证结果填写"}
                        ]
                    },
                    {
                        "id": "2.5", "name": "异常单结案",
                        "desc": "处置验证通过后，进入【结案记录】界面。输入本次异常单的结案描述，点击确定完成结案。异常单状态变更为「已结案」，处置流程结束。",
                        "remark": "",
                        "images": [
                            {"img": "fig-21.png", "desc": "结案记录"},
                            {"img": "fig-22.png", "desc": "结案完成"}
                        ]
                    }
                ]
            }
        ],
        "notes": [
            "检验员只对 QMS 单据判定界面进行操作，其余发起检验单操作不由检验员进行。",
            "异常单的每一步指派与处置结果均可发送邮箱提醒。",
            "IQC 检验前端作业流程与 PQC 一致，但单据由 ERP 发起。",
            "图片文件位于 images/quality/ 目录，替换对应图片即可更新。"
        ]
    },
}

MODULE_ORDER = [
    "injection", "assembly", "equipment", "mold",
    "quality"
]


# ============================================================
# HTML 渲染
# ============================================================

def esc(text):
    """HTML escape"""
    if text is None:
        return ""
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("\"", "&quot;")
    return text


def render_scenario(paragraphs):
    html = '<div class="section-content scenario-content">\n'
    for p in paragraphs:
        html += f'  <p>{esc(p)}</p>\n'
    html += '</div>\n'
    return html


def render_flowchart(img_dir, steps_list):
    """流程图：始终使用自动生成的 SVG（步骤配图保留在目录中供调用）"""
    svg = generate_svg_flowchart(steps_list)
    return f'<div class="section-content flowchart-content">\n{svg}\n</div>\n'


def generate_svg_flowchart(steps_list):
    """根据主步骤+子步骤生成横向 SVG 流程图（从左到右）"""
    if not steps_list:
        return '<p class="no-image">（无步骤数据）</p>'

    main_w = 170
    sub_w = 155
    main_h = 28
    sub_h = 20
    arrow_w = 20    # 主步骤之间箭头宽度
    col_gap = 16    # 箭头后到下一列间距
    col_pitch = main_w + arrow_w + col_gap  # 每列总宽
    pad_lr = 24     # 左右边距
    pad_top = 20
    sub_gap = 4     # 子步骤间距

    n = len(steps_list)
    total_w = pad_lr * 2 + col_pitch * (n - 1) + main_w

    # 找出子步骤最多的列
    max_subs = max(len(s["sub_steps"]) for s in steps_list)
    main_row_h = main_h + 12  # 主步骤行高度 + 到子步骤的间距
    if max_subs > 0:
        sub_area_h = max_subs * (sub_h + sub_gap) - sub_gap
        total_h = pad_top + main_row_h + sub_area_h + pad_top
    else:
        total_h = pad_top + main_row_h + pad_top

    main_row_y = pad_top
    sub_start_y = main_row_y + main_h + 10

    svg = f'<svg class="flowchart-svg" viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg">\n'
    svg += '  <defs>\n'
    svg += '    <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">\n'
    svg += '      <polygon points="0 0, 8 3, 0 6" fill="#1a73e8"/>\n'
    svg += '    </marker>\n'
    svg += '    <filter id="shadow" x="-4%" y="-4%" width="108%" height="108%">\n'
    svg += '      <feDropShadow dx="0" dy="1" stdDeviation="1.5" flood-opacity="0.12"/>\n'
    svg += '    </filter>\n'
    svg += '  </defs>\n'

    for i, step in enumerate(steps_list):
        box_x = pad_lr + i * col_pitch
        cx = box_x + main_w // 2

        # --- 主步骤：深蓝圆角矩形 ---
        svg += f'  <rect x="{box_x}" y="{main_row_y}" width="{main_w}" height="{main_h}" rx="6" fill="#1a73e8" filter="url(#shadow)"/>\n'
        svg += f'  <text x="{cx}" y="{main_row_y + main_h//2 + 4}" text-anchor="middle" fill="#fff" font-size="11" font-weight="700">{esc(step["title"])}</text>\n'

        # --- 水平箭头到下一个主步骤 ---
        if i < n - 1:
            ax1 = box_x + main_w
            ax2 = ax1 + arrow_w
            ay = main_row_y + main_h // 2
            svg += f'  <line x1="{ax1}" y1="{ay}" x2="{ax2}" y2="{ay}" stroke="#1a73e8" stroke-width="1.5" marker-end="url(#arrowhead)"/>\n'

        # --- 子步骤 ---
        sub_steps = step.get("sub_steps", [])
        for j, sub in enumerate(sub_steps):
            sy = sub_start_y + j * (sub_h + sub_gap)
            sx = cx - sub_w // 2

            # 子步骤：浅蓝圆角矩形
            svg += f'  <rect x="{sx}" y="{sy}" width="{sub_w}" height="{sub_h}" rx="4" fill="#e8f0fe" stroke="#1a73e8" stroke-width="1" filter="url(#shadow)"/>\n'
            svg += f'  <text x="{cx}" y="{sy + sub_h//2 + 3}" text-anchor="middle" fill="#1a73e8" font-size="9" font-weight="500">{esc(f"{sub["id"]} {sub["name"]}")}</text>\n'

            # 垂直箭头（主步骤 → 第一个子步骤，或子步骤之间）
            if j == 0:
                vy1 = main_row_y + main_h
                vy2 = sy
                if vy2 - vy1 > 4:
                    svg += f'  <line x1="{cx}" y1="{vy1}" x2="{cx}" y2="{vy2}" stroke="#1a73e8" stroke-width="1" marker-end="url(#arrowhead)"/>\n'
            else:
                prev_sy = sub_start_y + (j - 1) * (sub_h + sub_gap)
                vy1 = prev_sy + sub_h
                vy2 = sy
                svg += f'  <line x1="{cx}" y1="{vy1}" x2="{cx}" y2="{vy2}" stroke="#1a73e8" stroke-width="1" marker-end="url(#arrowhead)"/>\n'

    svg += '</svg>\n'
    return svg


def render_steps(steps_list, img_dir):
    html = '<div class="section-content steps-content">\n'
    for step_group in steps_list:
        title = step_group["title"]
        html += f'  <h3 class="step-group-title">{esc(title)}</h3>\n'
        for sub in step_group["sub_steps"]:
            sid = sub["id"]
            sname = sub["name"]
            sdesc = sub.get("desc", "")
            sremark = sub.get("remark", "")
            images = sub.get("images", [])

            # --- 子步骤头 ---
            html += f'  <div class="sub-step-header">{esc(sid)} {esc(sname)}</div>\n'

            # --- 图片区 ---
            if images:
                html += '  <div class="step-pair">\n'
                html += '    <div class="step-pair-imgs">\n'
                for img_item in images:
                    img_file = img_item["img"]
                    img_desc = img_item.get("desc", "")
                    img_path_full = os.path.join(BASE_DIR, img_dir, img_file)
                    html += '      <figure class="step-figure">\n'
                    if os.path.exists(img_path_full):
                        html += f'        <img src="../{img_dir}/{img_file}" alt="{esc(img_desc)}">\n'
                    else:
                        html += f'        <div class="placeholder-box">{esc(img_desc or "图片待添加")}</div>\n'
                    if img_desc:
                        html += f'        <figcaption>{esc(img_desc)}</figcaption>\n'
                    html += '      </figure>\n'
                html += '    </div>\n'
                # --- 文字区 ---
                html += '    <div class="step-pair-text">\n'
                html += f'      <div class="step-desc"><strong>作业说明：</strong>{esc(sdesc)}</div>\n'
                if sremark:
                    html += f'      <div class="step-remark"><strong>备注：</strong>{esc(sremark)}</div>\n'
                html += '    </div>\n'
                html += '  </div>\n'
            else:
                # 无图片
                html += '  <div class="step-pair">\n'
                html += '    <div class="step-pair-text">\n'
                html += f'      <div class="step-desc"><strong>作业说明：</strong>{esc(sdesc)}</div>\n'
                if sremark:
                    html += f'      <div class="step-remark"><strong>备注：</strong>{esc(sremark)}</div>\n'
                html += '    </div>\n'
                html += '  </div>\n'

    html += '</div>\n'
    return html


def render_notes(note_list):
    if not note_list:
        return ""
    html = '<div class="section-content notes-content">\n  <ul>\n'
    for n in note_list:
        if n.strip():
            html += f'    <li>{esc(n.strip())}</li>\n'
    html += '  </ul>\n</div>\n'
    return html


# ============================================================
# 页面模板
# ============================================================

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - MES操作指导书</title>
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <div class="layout">
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <a href="../index.html" class="sidebar-home-link">
          <h2 class="sidebar-title">美诗儿 MES 操作指导书</h2>
        </a>
      </div>
      <nav class="sidebar-modules">
        <ul>
          {module_nav}
        </ul>
      </nav>
      <div class="sidebar-divider"></div>
      <nav class="sidebar-sections">
        <div class="sidebar-section-label">本页目录</div>
        <ul>
          {page_toc}
        </ul>
      </nav>
    </aside>
    <main class="main-content" id="main-content">
      <header class="page-header">
        <h1>{title}</h1>
        <div class="meta-info">部门：{dept}</div>
      </header>
      <div class="sections">
        {sections_html}
      </div>
      <footer class="page-footer">
        <p>美诗儿（浙江）环境智能电器有限公司 - MES 操作指导书</p>
        <p class="footer-edit-hint">提示：图片文件位于 <code>{img_dir}/</code> 目录，替换对应图片即可更新</p>
      </footer>
    </main>
  </div>
  <script src="../js/main.js"></script>
</body>
</html>"""

SECTION_TMPL = """      <section class="doc-section" id="{id}">
        <h2 class="section-title">{name}</h2>
        {content}
      </section>"""


def generate_module_html(key, mod):
    sections_html = ""

    # 场景说明
    sections_html += SECTION_TMPL.format(
        id="scenario", name="场景说明",
        content=render_scenario(mod["scenario"])
    )

    # 流程图（始终显示，无图片时自动生成 SVG）
    fc = render_flowchart(mod["img_dir"], mod["steps"])
    sections_html += SECTION_TMPL.format(
        id="flowchart", name="流程图", content=fc
    )

    # 操作步骤
    steps = render_steps(mod["steps"], mod["img_dir"])
    sections_html += SECTION_TMPL.format(
        id="steps", name="操作步骤说明", content=steps
    )

    # 注意事项
    notes = render_notes(mod.get("notes", []))
    if notes:
        sections_html += SECTION_TMPL.format(
            id="notes", name="注意事项", content=notes
        )

    # 模块导航（左侧所有模块列表）
    module_nav = ""
    for k in MODULE_ORDER:
        m = CONTENT[k]
        active_class = ' class="active"' if k == key else ""
        module_nav += f'      <li><a href="../pages/{k}.html"{active_class}>{m["icon"]} {esc(m["title"])}</a></li>\n'

    # 本页目录 ToC
    toc_items = [
        ("scenario", "场景说明"),
        ("flowchart", "流程图"),
        ("steps", "操作步骤说明"),
        ("notes", "注意事项"),
    ]
    page_toc = ""
    for tid, tname in toc_items:
        if tid == "notes" and not mod.get("notes", []):
            continue
        page_toc += f'      <li><a href="#{tid}">{tname}</a></li>\n'

    html = PAGE_TEMPLATE.format(
        title=esc(mod["title"]),
        dept=esc(mod["dept"]),
        module_nav=module_nav,
        page_toc=page_toc,
        sections_html=sections_html,
        img_dir=mod["img_dir"],
    )

    out_path = os.path.join(BASE_DIR, "pages", f"{key}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ 已生成: pages/{key}.html")


def generate_index():
    toc_items = ""
    cards = ""
    for key in MODULE_ORDER:
        mod = CONTENT[key]
        toc_items += f'      <li><a href="pages/{key}.html">{mod["icon"]} {esc(mod["title"])}</a></li>\n'
        cards += f'''    <a href="pages/{key}.html" class="module-card">
      <div class="card-icon">{mod["icon"]}</div>
      <div class="card-body">
        <h3>{esc(mod["title"])}</h3>
        <p class="card-dept">{esc(mod["dept"])}</p>
      </div>
    </a>\n'''

    INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>美诗儿 MES 操作指导书</title>
<link rel="stylesheet" href="css/style.css">
</head>
<body class="index-page">
  <div class="index-layout">
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <h2 class="sidebar-title">美诗儿 MES 操作指导书</h2>
      </div>
      <nav class="sidebar-modules">
        <ul>
          {index_toc}
        </ul>
      </nav>
    </aside>
    <main class="main-content">
      <header class="page-header index-header">
        <h1>美诗儿（浙江）环境智能电器有限公司</h1>
        <p class="subtitle">MES 系统操作指导书</p>
        <p class="desc">本手册包含以下操作模块，点击模块卡片或侧边栏目录查看详细内容。</p>
      </header>
      <div class="module-grid">
        {module_cards}
      </div>
      <footer class="page-footer">
        <p>美诗儿（浙江）环境智能电器有限公司 - MES 操作指导书</p>
        <p class="footer-edit-hint">提示：将需要替换的图片放入对应 images/ 子目录，保持文件名一致即可</p>
      </footer>
    </main>
  </div>
  <script src="js/main.js"></script>
</body>
</html>"""

    html = INDEX_HTML.format(index_toc=toc_items, module_cards=cards)
    out_path = os.path.join(BASE_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ 已生成: index.html")


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 60)
    print("MES 操作指导书 HTML 生成器 v3")
    print("8 模块完整内容 + 层级子步骤")
    print("=" * 60)

    os.makedirs(os.path.join(BASE_DIR, "pages"), exist_ok=True)
    for mod in CONTENT.values():
        os.makedirs(os.path.join(BASE_DIR, mod["img_dir"]), exist_ok=True)

    for key in MODULE_ORDER:
        mod = CONTENT[key]
        print(f"\n▶ 正在生成: {mod['title']}")
        step_count = sum(len(sg["sub_steps"]) for sg in mod["steps"])
        print(f"  共 {len(mod['steps'])} 个主步骤, {step_count} 个子步骤")
        generate_module_html(key, mod)

    print("\n▶ 正在生成总目录...")
    generate_index()

    print("\n" + "=" * 60)
    print("全部生成完毕！共 {} 个模块".format(len(MODULE_ORDER)))
    print("=" * 60)


if __name__ == "__main__":
    main()
