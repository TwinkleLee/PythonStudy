# 运行
1. python bCNC
打开UI界面调整激光头位置
2. cd bCNC
3. python GcodeSender

# 文件
`bCNC/GcodeSender.py`做了修改 并引用了`bCNC/lib/troncellTest.py`
注意`GetNextOrderGcodeFile`接口入参中的type,传任意值都表示4代,不传表示3代
`myDocuments`目录中为电路图和一些demo
