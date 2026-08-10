import requests
import sqlite3
import hashlib
import os
import subprocess
from datetime import datetime

# 从仓库Secrets读取token，代码内不明文写入密钥
GITHUB_TOKEN = os.getenv("GH_TOKEN")
OUTPUT_PY = "./launcher_list.py"
DB_FILE = "./launcher_cache.db"
QUERY = "minecraft android launcher language:python"
MODRINTH_CATEGORY = "launcher"

def init_sqlite():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS launcher_store(
        proj_id TEXT PRIMARY KEY,
        name TEXT,
        source TEXT,
        link TEXT,
        verify_hash TEXT,
        last_check TEXT
    )
    ''')
    conn.commit()
    conn.close()

def md5_hash(data: str):
    return hashlib.md5(data.encode("utf-8")).hexdigest()

def pull_github_repo():
    header = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else dict()
    resp = requests.get(f"https://api.github.com/search/repositories?q={QUERY}&per_page=30", headers=header, timeout=25)
    res_list = []
    if resp.status_code == 200:
        for repo in resp.json()["items"]:
            res_list.append({
                "proj_id": repo["full_name"],
                "name": repo["name"],
                "source": "github",
                "link": repo["html_url"],
                "sign": repo["pushed_at"]
            })
    return res_list

def pull_modrinth():
    api_url = f'https://api.modrinth.com/v2/search?facets=[["categories:{MODRINTH_CATEGORY}"]]&limit=30'
    resp = requests.get(api_url,timeout=25)
    res_list = []
    if resp.status_code == 200:
        for item in resp.json()["hits"]:
            res_list.append({
                "proj_id": item["project_id"],
                "name": item["title"],
                "source": "modrinth",
                "link": f"https://modrinth.com/project/{item['slug']}",
                "sign": str(item["updated"])
            })
    return res_list

def judge_add_update(raw_data):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    add_arr = []
    update_arr = []
    time_now = datetime.now().isoformat()
    for info in raw_data:
        h = md5_hash(info["sign"])
        cur.execute("SELECT verify_hash FROM launcher_store WHERE proj_id = ?",(info["proj_id"],))
        row = cur.fetchone()
        if not row:
            add_arr.append(info)
            cur.execute("INSERT INTO launcher_store(proj_id,name,source,link,verify_hash,last_check) VALUES (?,?,?,?,?,?)",
                        (info["proj_id"],info["name"],info["source"],info["link"],h,time_now))
        else:
            if row[0] != h:
                update_arr.append(info)
                cur.execute("UPDATE launcher_store SET verify_hash=?,last_check=? WHERE proj_id=?",(h,time_now,info["proj_id"]))
    conn.commit()
    conn.close()
    return add_arr,update_arr

def refresh_list_file(new_items):
    init_content = "# MC安卓启动器开源项目列表 | Actions每5h自动采集 禁止手动修改\nlauncher_list = []\n"
    if os.path.exists(OUTPUT_PY):
        with open(OUTPUT_PY,"r",encoding="utf-8") as f:
            file_ctx = f.read()
    else:
        file_ctx = init_content
    import ast
    try:
        slice_start = file_ctx.find("launcher_list = [")
        slice_end = file_ctx.rfind("]")
        old_data = ast.literal_eval(file_ctx[slice_start:slice_end+1].split("=")[1])
    except:
        old_data = []
    for item in new_items:
        cell = {
            "id":item["proj_id"],
            "name":item["name"],
            "platform":item["source"],
            "url":item["link"]
        }
        old_data.append(cell)
    new_ctx = f"launcher_list = {repr(old_data)}\n"
    final_text = file_ctx.split("launcher_list = ")[0] + new_ctx
    with open(OUTPUT_PY,"w",encoding="utf-8") as f:
        f.write(final_text)

def git_commit_push():
    # 配置git提交用户信息，提交改动文件
    subprocess.run(["git","config","user.name","auto-bot"])
    subprocess.run(["git","config","user.email","bot@actions.com"])
    subprocess.run(["git","add","launcher_list.py","launcher_cache.db"])
    subprocess.run(["git","commit","-m","auto update launcher list"])
    subprocess.run(["git","push"])

if __name__ == "__main__":
    init_sqlite()
    github_data = pull_github_repo()
    mod_data = pull_modrinth()
    all_data = github_data + mod_data
    add,update = judge_add_update(all_data)
    print(f"本次采集：新增项目{len(add)} | 版本更新项目{len(update)}")
    if len(add) > 0:
        refresh_list_file(add)
        git_commit_push()
    else:
        print("本轮检索无新项目，无需提交仓库")
