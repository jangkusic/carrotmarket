const form = document.querySelector("#login-form");

let accessToken = null;

// 비밀번호 해시로 암호화하는 방법
const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);
  // console.log(formData.get("password"));

  const div = document.querySelector("#info");

  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });
  const data = await res.json();
  const accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);
  alert("로그인되었습니다.");

  // const infoDiv = document.querySelector("#info");
  // infoDiv.innerText = "로그인 되었습니다.";

  window.location.pathname = "/";

  // const btn = document.createElement("button");
  // btn.innerText = "상품 가져오기";
  // btn.addEventListener("click", async () => {
  //   const res = await fetch("/items", {
  //     headers: {
  //       Authorization: "Bearer ${acessToken}",
  //     },
  //   });
  //   const data = await res.json();
  //   console.log(data);
  // });
  // infoDiv.appendChild(btn);

  // console.log(accessToken);

  // 서버에서 자동으로 status를 200으로 보내줌
  // if (res.status === 200) {
  //   alert("로그인에 성공했습니다.");
  //   // window.location.pathname = "/";
  //   console.log(res.status);
  //   //   console.log(data);
  //   //   window.location.pathname = "/login.html";
  //   //   div.innerText = "회원가입에 성공했습니다.";
  //   //   div.style.color = "blue";
  // } else if (res.status === 401) {
  //   alert("아이디 혹은 패스워드가 틀렸습니다.");
  // }
  // // }
};
form.addEventListener("submit", handleSubmit);
