function setPreferredColorScheme(mode = "dark") {
    console.log("changing")
    for (var i = document.styleSheets[0].rules.length - 1; i >= 0; i--) {
        rule = document.styleSheets[0].rules[i].media;
        if (rule.mediaText.includes("prefers-color-scheme")) {
            console.log("includes color scheme")
            switch (mode) {
                case "light":
                    console.log("light")
                    rule.appendMedium("original-prefers-color-scheme");
                    if (rule.mediaText.includes("light")) rule.deleteMedium("(prefers-color-scheme: light)");
                    if (rule.mediaText.includes("dark")) rule.deleteMedium("(prefers-color-scheme: dark)");
                    break;
                case "dark":
                    console.log("dark")
                    rule.appendMedium("(prefers-color-scheme: light)");
                    rule.appendMedium("(prefers-color-scheme: dark)");
                    if (rule.mediaText.includes("original")) rule.deleteMedium("original-prefers-color-scheme");
                    break;
                default:
                    console.log("default")
                    rule.appendMedium("(prefers-color-scheme: dark)");
                    if (rule.mediaText.includes("light")) rule.deleteMedium("(prefers-color-scheme: light)");
                    if (rule.mediaText.includes("original")) rule.deleteMedium("original-prefers-color-scheme");
            }
            break;
        }
    }
}
