const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault();

  const body = new FormData(form);
  // body에 insertAt 값을 추가하기 위해 body 변수를 만들어서
  // append 함수를 만들어서 추가함.
  // 세계시간
  body.append("insertAt", new Date().getTime());
  try {
    const res = await fetch("items", {
      method: "POST",
      // 자바스크립트에서는 body:body를 body로만 작성해도 됨.
      // 즉, 이름이 똑같으면 하나만 작성하면 됨.
      body: body,
    });
    const data = await res.json();
    if (data === "200") window.location.pathname = "/";
  } catch (e) {
    console.error;
  }
};

form.addEventListener("submit", handleSubmitForm);

// const handleSubmitForm = async (event) => {
//   event.preventDefault();
//      await fetch("items", {
//       method: "POST",
//       body: new FormData(form),
//     });

// };

// form.addEventListener("submit", handleSubmitForm);
