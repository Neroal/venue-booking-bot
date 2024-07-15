document.getElementById('submit').addEventListener('click', () => {
    const account = document.getElementById('account').value;
    const password = document.getElementById('password').value;
    const timeSlot = document.getElementById('timeSlot').value;
    
    let d2;
    if (timeSlot === "06:00~07:00" || timeSlot === "07:00~08:00" || timeSlot === "08:00~09:00" || timeSlot === "09:00~10:00" || 
        timeSlot === "10:00~11:00" || timeSlot === "11:00~12:00") {
      d2 = 1;
    } else if (timeSlot === "17:00~18:00" || timeSlot === "18:00~19:00" || timeSlot === "19:00~20:00" || timeSlot === "20:00~21:00") {
      d2 = 2;
    } else if (timeSlot === "21:00~22:00") {
      d2 = 3;
    } else {
      d2 = 1; // Default value if time slot does not match any condition
    }
  
    document.getElementById('output').innerText = "";
    window.electron.send('run-python', { account, password, timeSlot, d2 });
  });
  
  window.electron.receive('python-output', (message) => {
    document.getElementById('output').innerText = message;
  });
  