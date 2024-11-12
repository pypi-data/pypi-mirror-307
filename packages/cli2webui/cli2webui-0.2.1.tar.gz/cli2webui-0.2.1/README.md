# CLI2WebUI

将命令行工具转换为Web界面的工具。

## 安装

```bash
pip install cli2webui
```

## 使用方法

基本用法：
```bash
cli2webui <command>
```

例如：
```bash
cli2webui ls  # 将ls命令转换为web界面
cli2webui --port 5600 ls  # 在指定端口运行
cli2webui --host 0.0.0.0 --port 8080 ls  # 指定主机和端口
```

支持的参数：
- `--port`: 指定web服务器端口（默认：5000）
- `--host`: 指定web服务器主机（默认：localhost）

## 功能特点

- 自动解析命令行工具的帮助信息
- 生成交互式Web界面
- 实时显示命令执行输出
- 支持自定义端口和主机
- 支持大多数常见的命令行工具

## 工作原理

CLI2WebUI 通过以下步骤工作：

1. 解析命令行工具的帮助信息
2. 生成对应的Web表单界面
3. 启动本地Web服务器
4. 执行用户通过Web界面提交的命令
5. 实时显示命令执行结果

## 开发

要参与开发，请按以下步骤操作：

```bash
# 克隆仓库
git clone https://github.com/wangmaobin/cli2webui.git

# 安装开发依赖
cd cli2webui
pip install -e .

# 运行测试
python -m pytest
```

## 许可证

MIT License

## 作者

Wang Maobin (wangmaobin@iscas.ac.cn)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v0.2.0
- 支持自定义端口和主机
- 改进了命令行参数处理
- 优化了web界面响应性
- 添加了更多命令行工具支持

### v0.1.0
- 初始版本发布
- 基本的命令行转Web功能
- 支持实时输出显示