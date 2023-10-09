document.addEventListener("DOMContentLoaded", function () {
  const fromFormatDropdown = document.getElementById("from-format");
  const epubOption = document.getElementById("epub");
  const pdfOption = document.getElementById("pdf");
  const jpgOption = document.getElementById("jpg");
  const pngOption = document.getElementById("png");
  const txtOption = document.getElementById("txt");
  const convertButton = document.getElementById("convert-btn");
  const outputDiv = document.getElementById("output");

  function updateOptionVisibility() {
    // Hide all options initially
    epubOption.style.visibility = "hidden";
    jpgOption.style.visibility = "hidden";
    pngOption.style.visibility = "hidden";
    txtOption.style.visibility = "hidden";

    const fromFormat = fromFormatDropdown.value;

    // Show options based on selected 'from format'
    if (fromFormat === "pdf") {
      epubOption.style.visibility = "visible";
      txtOption.style.visibility = "visible";
    }
    if (fromFormat === "txt") {
      pdfOption.style.visibility = "visible";
      epubOption.style.visibility = "hidden";
    }
    if (fromFormat === "png") {
      pdfOption.style.visibility = "visible";
      epubOption.style.visibility = "hidden";
      jpgOption.style.visibility = "visible";
    }
    if (fromFormat === "jpeg") {
      pdfOption.style.visibility = "visible";
      epubOption.style.visibility = "hidden";
      pngOption.style.visibility = "visible";
    }
  }

  // Initial update
  updateOptionVisibility();

  // Update the visibility of options whenever the selected value changes
  fromFormatDropdown.addEventListener("change", updateOptionVisibility);

  convertButton.addEventListener("click", function () {
    const fromFormat = fromFormatDropdown.value;
    const toFormat = document.getElementById("to-format").value;
    const inputFile = document.getElementById("file-input").files[0];
    if (inputFile) {
      const convertedText = `Wait! Conversion from ${fromFormat} to ${toFormat} is in process...`;
      outputDiv.textContent = convertedText;
    } else {
      outputDiv.textContent = "Please select a file.";
    }
  });
});
