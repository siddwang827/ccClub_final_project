
// liff.init({
//   liffId: '1656063313-2ZQLeoMW'
// }).then(function() {
//   liff.getProfile()
// .then(profile => {
//   const name = profile.displayName;
//   const userID = profile.userId;
//   console.log(name);
//   console.log(userID);
// })
// .catch((err) => {
//   console.log('error', err);
// });
//   var profile = liff.getProfile();
//   console.log(profile)
//   console.log('LIFF init');
  
// }).catch(function(error) {
  
//   console.log(error);
// });


liff.init({
  　liffId: '1656063313-2ZQLeoMW'
  }) .then(() => {
    if (!liff.isLoggedIn()) {
      alert("巨巨目前尚未登入哦~");
      liff.login();
    } else {
      liff.getProfile()
      .then(profile => {
      const username = profile.displayName;
      // const userid = profile.userId
      alert('\nHi '+ username +'~\n\n歡迎回來~');
      const accessToken = liff.getAccessToken();
      document.getElementById("access_token").value = accessToken
      document.getElementById("line_name").value = username;
      }
    )}
  }).catch((err) => {
    console.log('初始化失敗')
  });



// // function sendForm() {
// //   var sform = document.forms['form1']
// //   sform.append('access_token', accessToken)

// //   $.ajax({
// //     url:"https://f99c6c53e900.ngrok.io/routine_submit",
// //     type:"POST",
// //     data:JSON.stringify,
// //     contentType: "application/json",
// //     dataType:'json',
//   // success:function(){
// })
// }