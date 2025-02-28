const API_URL = "https://libretranslate.com/languages";

var basic_languages = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
};

async function fetchLanguages() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error("Failed to fetch languages");
        }
        const languages = await response.json();
        populateLanguageDropdowns(languages);
    } catch (error) {
        console.error("Error fetching languages:", error);
        console.log("Using default languages.");
        populateLanguageDropdownsFromDefaults();
    }
}

function populateLanguageDropdowns(languages) {
    const inputLangSelect = document.getElementById("input_language");
    const outputLangSelect = document.getElementById("output_language");

    languages.forEach(lang => {
        const optionInput = document.createElement("option");
        optionInput.value = lang.code;
        optionInput.textContent = lang.name;
        inputLangSelect.appendChild(optionInput);

        const optionOutput = document.createElement("option");
        optionOutput.value = lang.code;
        optionOutput.textContent = lang.name;
        outputLangSelect.appendChild(optionOutput);
    });
}

function populateLanguageDropdownsFromDefaults() {
    const inputLangSelect = document.getElementById("input_language");
    const outputLangSelect = document.getElementById("output_language");

    Object.entries(basic_languages).forEach(([code, name]) => {
        const optionInput = document.createElement("option");
        optionInput.value = code;
        optionInput.textContent = name;
        inputLangSelect.appendChild(optionInput);

        const optionOutput = document.createElement("option");
        optionOutput.value = code;
        optionOutput.textContent = name;
        outputLangSelect.appendChild(optionOutput);
    });
}

fetchLanguages();
