const resumeAction = document.getElementById('resume-action');

resumeAction?.addEventListener('click', (event) => {
  if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;

  const today = new Date();
  const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  const date = `${String(today.getDate()).padStart(2, '0')}${months[today.getMonth()]}${today.getFullYear()}`;
  const download = document.createElement('a');
  download.href = resumeAction.href;
  download.download = `Rasheed_Abdul_Haq_Kozhiparamban_${date}.pdf`;
  document.body.append(download);
  download.click();
  download.remove();
  // The original link still opens the PDF viewer in a new tab.
});
