const JSON_URL = "https://cdn.jsdelivr.net/gh/wdsj1314/mc‑launcher‑lis@main/list.json?t="+Date.now();

async function loadData(){
  const domLoading = document.querySelector("#loading");
  const domList = document.querySelector("#list");
  try{
    const resp = await fetch(JSON_URL);
    const arr = await resp.json();
    domLoading.remove();
    arr.forEach(item=>{
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        <h3>${item.name}</h3>
        <p>${item.desc||""}</p>
        <a href="${item.url}" target="_blank">前往下载</a>
      `;
      domList.appendChild(div);
    })
  }catch(e){
    domLoading.innerText="数据加载失败";
    console.error(e);
  }
}
loadData();
