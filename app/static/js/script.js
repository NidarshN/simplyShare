// Index Page

window.history.forward();

console.log("Hello");
const showSidebar = () => {
    const sidebar = document.getElementById("sidebar");
    sidebar.style.display = "flex";
    const menu_icon = document.getElementById("menu");
    menu_icon.style.visibility = "hidden";
};

const hideSidebar = () => {
    const sidebar = document.getElementById("sidebar");
    sidebar.style.display = "none";
    const menu_icon = document.getElementById("menu");
    menu_icon.style.visibility = "visible";
};

// Login Page

const validateUser = (event) => {
    event.preventDefault();
    let formElement = document.getElementById("loginForm");
    let usernameElement = document.getElementById("username");
    let passwordElement = document.getElementById("password");

    let usrname = usernameElement.value;

    axios
        .post(
            "/validateUser",
            { username: usrname, password: passwordElement.value },
            {
                headers: {
                    "content-type": "application/json",
                },
            }
        )
        .then((res) => {
            if (res.data.valid_credentials == "false") {
                alert("Invalid Credentials");
                usernameElement.value = "";
                passwordElement.value = "";
            } else {
                sessionStorage.setItem("user_sessionID", res.data.session_id);
                sessionStorage.setItem("user", usrname);
                location.href = "/home";
            }
        })
        .catch((error) => {
            console.log(error);
        });
};

// Registration Page
function toggleVisiblity() {
    let passwdElement = document.getElementById("passwd");
    let confirmPasswdElement = document.getElementById("confirmPasswd");
    let passwdIcon = document.getElementById("passwdIcon");
    let cpasswdIcon = document.getElementById("cpasswdIcon");

    if (passwdElement.type === "password") {
        passwdElement.type = "text";
        confirmPasswdElement.type = "text";
        passwdIcon.classList.replace("bxs-lock-alt", "bxs-lock-open-alt");
        cpasswdIcon.classList.replace("bxs-lock-alt", "bxs-lock-open-alt");
    } else {
        passwdElement.type = "password";
        confirmPasswdElement.type = "password";
        passwdIcon.classList.replace("bxs-lock-open-alt", "bxs-lock-alt");
        cpasswdIcon.classList.replace("bxs-lock-open-alt", "bxs-lock-alt");
    }
}

const validateFields = (event) => {
    event.preventDefault();
    let firstname = document.getElementById("firstname");
    let lastname = document.getElementById("lastname");
    let username = document.getElementById("username");
    let email = document.getElementById("email");
    let passwd = document.getElementById("passwd");
    let confirmPasswd = document.getElementById("confirmPasswd");

    if (
        firstname.value != "" &&
        lastname.value != "" &&
        username.value != "" &&
        passwd.value != "" &&
        confirmPasswd.value != ""
    ) {
        if (passwd.value === confirmPasswd.value) {
            username.style = "border: 2px solid rgba(255,255,255,0.2);";
            passwd.style = "border: 2px solid rgba(255,255,255,0.2);";
            confirmPasswd.style = "border: 2px solid rgba(255,255,255,0.2);";

            registerUser(firstname, lastname, username, email, confirmPasswd);
        }
    } else {
        firstname.style =
            firstname == ""
                ? "border: 2px solid rgba(255,0,0,0.2);"
                : "border: 2px solid rgba(0,255,0,0.2);";
        lastname.style =
            lastname == ""
                ? "border: 2px solid rgba(255,0,0,0.2);"
                : "border: 2px solid rgba(0,255,0,0.2);";
        email.style =
            email == ""
                ? "border: 2px solid rgba(255,0,0,0.2);"
                : "border: 2px solid rgba(0,255,0,0.2);";
        username.style =
            username == ""
                ? "border: 2px solid rgba(255,0,0,0.2);"
                : "border: 2px solid rgba(0,255,0,0.2);";
        passwd.style =
            passwd == ""
                ? "border: 2px solid rgba(255,0,0,0.2);"
                : "border: 2px solid rgba(0,255,0,0.2);";
        confirmPasswd.style =
            confirmPasswd == ""
                ? "border: 2px solid rgba(255,0,0,0.2);"
                : "border: 2px solid rgba(0,255,0,0.2);";
    }
};

const checkCPasswd = () => {
    let passwdElement = document.getElementById("passwd");
    let confirmPasswdElement = document.getElementById("confirmPasswd");

    if (passwdElement.value != confirmPasswdElement.value) {
        confirmPasswd.style = "border: 2px solid rgba(255,0,0,0.2);";
    } else {
        confirmPasswd.style = "border: 2px solid rgba(0,255,0,0.2);";
        passwdElement.style = "border: 2px solid rgba(0,255,0,0.2);";
        if (sessionStorage["enableSubmit"] == "true") {
            document.getElementById("registerBtn").disabled = false;
        }
    }
};

const registerUser = (firstname, lastname, username, email, confirmPasswd) => {
    axios
        .post(
            "/registeruser",
            {
                firstname: firstname.value,
                lastname: lastname.value,
                username: username.value,
                email: email.value,
                password: confirmPasswd.value,
            },
            {
                headers: { "Content-Type": "application/json" },
            }
        )
        .then((res) => {
            if (res.data.isuserregistered == "true") {
                alert("User Registered Successfully! Routing to login!");
                resetForm();
                location.href = "/signin";
            } else {
                alert("Error: cannot register user!");
                resetForm();
                location.href = "/signup";
            }
        })
        .catch((error) => {
            alert("Unable to register user!");
            console.log(error);
        });
};

const checkUnique = () => {
    let usernameElement = document.getElementById("username");
    let username = usernameElement.value;

    if (username != "") {
        axios
            .post(
                "/checkunique",
                { username: username },
                {
                    headers: {
                        "content-type": "application/json",
                    },
                }
            )
            .then((res) => {
                if (res.data.isunique == "false") {
                    alert("Please enter a unique username!");
                    usernameElement.value = "";
                    usernameElement.style =
                        "border: 2px solid rgba(255, 255, 255, 0.2);";
                } else {
                    usernameElement.style =
                        "border: 2px solid rgba(0, 255, 0, 0.2);";
                }
            })
            .catch((error) => {
                console.log(error);
            });
    }
};

const validateEmailWrapper = async () => {
    let emailElement = document.getElementById("email");
    let email = emailElement.value;
    let passwdElement = document.getElementById("passwd");
    let confirmPasswdElement = document.getElementById("confirmPasswd");

    let isValid = validateEmail(email);

    if (!isValid) {
        alert("Please enter a valid email id!");
        emailElement.value = "";
    } else {
        alert(
            "Kindly check the email inbox and confirm the AWS Email Verification Request!"
        );
        await axios
            .post(
                "/registeremail",
                { email: email },
                {
                    headers: { "Content-Type": "application/json" },
                }
            )
            .then((response) => {
                if (response.data.isVerified == "true") {
                    alert("Email Registered Successfully!");
                    emailElement.disabled = true;
                    sessionStorage["enableSubmit"] = true;
                    emailElement.style =
                        "border: 2px solid rgba(0, 255, 0, 0.2);";
                    if (
                        passwdElement.value != "" &&
                        confirmPasswdElement.value != "" &&
                        passwdElement.value == confirmPasswdElement.value
                    ) {
                        document.getElementById("registerBtn").disabled = false;
                    }
                } else {
                    sessionStorage["enableSubmit"] = false;
                    alert(
                        "Kindly check the email inbox and Try Again with the same email!"
                    );
                    emailElement.style =
                        "border: 2px solid rgba(255, 0, 0, 0.2);";
                }
            })
            .catch((error) => {
                alert(
                    "Email Verification Failed! Try with a new email address!"
                );
            });
    }
};

const resetForm = () => {
    let formElement = document.getElementById("registerForm");
    let formbtn = document.getElementById("registerBtn");
    formElement.reset();
    formbtn.disabled = true;
};

// Main page

const isAuthenticated = () => {
    if (
        sessionStorage.getItem("user_sessionID") == null &&
        sessionStorage.getItem("user") == null
    ) {
        location.href = "/signin";
    }
};
window.addEventListener("load", () => {
    let emailinp = document.getElementById("emailInput");

    if (emailinp) {
        emailinp.addEventListener("keydown", function (event) {
            if (event.key == "Enter") {
                if (event.cancelable) {
                    event.preventDefault();
                }
                addEmail();
            }
        });
    }

    let inp_FileUpload = document.querySelectorAll(".inputFileUpload");
    if (inp_FileUpload) {
        document
            .querySelectorAll(".inputFileUpload")
            .forEach((inputElement) => {
                const uploadAreaElement = inputElement.closest(".uploadArea");

                uploadAreaElement.addEventListener("click", (e) => {
                    inputElement.click();
                });

                inputElement.addEventListener("change", (e) => {
                    if (inputElement.files) {
                        updateThumbnail(
                            uploadAreaElement,
                            inputElement.files[0]
                        );
                    }
                });

                uploadAreaElement.addEventListener("dragover", (e) => {
                    if (e.cancelable) {
                        e.preventDefault();
                    }
                    uploadAreaElement.classList.add("uploadArea--over");
                });

                ["dragleave", "dragend"].forEach((type) => {
                    uploadAreaElement.addEventListener(type, (e) => {
                        uploadAreaElement.classList.remove("uploadArea--over");
                    });
                });

                uploadAreaElement.addEventListener("drop", (e) => {
                    if (e.cancelable) {
                        e.preventDefault();
                    }

                    if (e.dataTransfer.files.length) {
                        inputElement.files = e.dataTransfer.files;
                        inputElement.effectAllowed = inputElement.dropEffect =
                            "none";
                        updateThumbnail(
                            uploadAreaElement,
                            e.dataTransfer.files[0]
                        );
                    }

                    if (uploadAreaElement) {
                        uploadAreaElement.classList.remove("uploadArea--over");
                    }
                });
            });
    }
});

const createCard = (sender, recipient, file_name, fileurl, filetype, index) => {
    let spanCard = document.createElement("span");
    spanCard.className = "fileCardContent";
    spanCard.setAttribute("id", index);
    if (filetype == "own") {
        spanCard.setAttribute("onclick", "homeowndownload(event)");
    } else {
        spanCard.setAttribute("onclick", "homefiledownload(event)");
    }
    let spanIcon = document.createElement("i");
    let iconclass = checkExtension(file_name);
    spanIcon.className = "fileIcon " + iconclass;
    spanCard.appendChild(spanIcon);

    let pfilename = document.createElement("p");
    pfilename.className = "filename";
    pfilename.setAttribute("id", index + "_filename");
    pfilename.innerText = file_name;
    spanCard.appendChild(pfilename);

    let psender = document.createElement("p");
    psender.innerText = sender;
    psender.setAttribute("id", index + "_sender");
    psender.style = "display: none;";
    spanCard.appendChild(psender);

    let precipient = document.createElement("p");
    precipient.innerText = recipient;
    precipient.setAttribute("id", index + "_recipient");
    precipient.style = "display: none;";
    spanCard.appendChild(precipient);

    let pfileurl = document.createElement("p");
    pfileurl.innerText = fileurl;
    pfileurl.setAttribute("id", index + "_fileurl");
    pfileurl.style = "display: none;";
    spanCard.appendChild(pfileurl);
    return spanCard;
};

const addFile = (sender, recipient, file_name, fileurl, filetype, index) => {
    let customstyle = "";
    if (filetype == "own") {
        customstyle = "border: 2px dashed #1150ED";
    } else {
        customstyle = "border: 2px dashed #11EDAE";
    }
    let filegrid = document.getElementById("fileGrid");
    let n = filegrid.childElementCount;
    if (n == 0) {
        n += 1;
    }
    for (let i = 0; i < n; i++) {
        if (
            filegrid.childElementCount != 0 &&
            filegrid.children[i].childElementCount < 5
        ) {
            let newData = document.createElement("td");
            let newCard = document.createElement("div");
            newCard.className = "fileCard";
            newCard.style = customstyle;
            let newSpanCard = createCard(
                sender,
                recipient,
                file_name,
                fileurl,
                filetype,
                index
            );
            newCard.appendChild(newSpanCard);
            newData.appendChild(newCard);
            filegrid.children[i].appendChild(newData);
        } else {
            if (i != n - 1) {
                continue;
            } else {
                let newRow = document.createElement("tr");
                newRow.className = "cardRow";
                let newData = document.createElement("td");
                let newCard = document.createElement("div");
                newCard.className = "fileCard";
                newCard.style = customstyle;
                let newSpanCard = createCard(
                    sender,
                    recipient,
                    file_name,
                    fileurl,
                    filetype,
                    index
                );
                newCard.appendChild(newSpanCard);
                newData.appendChild(newCard);
                newRow.appendChild(newData);
                newRow.id = "fileGridRow_" + String(i + 1);
                filegrid.appendChild(newRow);
            }
        }
    }
};

const fetchdetails = () => {
    axios
        .post(
            "/displayhome",
            { user: sessionStorage.getItem("user_sessionID") },
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        )
        .then((response) => {
            let cardgrid = document.getElementById("cardgrid");
            let displayempty = document.getElementById("emptyind");
            if (response.data["route"] == "") {
                cardgrid.style = "display: flex;";
                displayempty.style = "display: none;";
                if (response.data["own"] != {}) {
                    let ftype = "own";
                    let own_data = response.data["own"];
                    for (let i = 0; i < own_data.length; i++) {
                        let ind = "own" + String(i);
                        if (own_data[i] != {}) {
                            let row_file = own_data[i];
                            addFile(
                                row_file["sender"],
                                row_file["recipient"],
                                row_file["filename"],
                                row_file["fileurl"],
                                ftype,
                                ind
                            );
                        }
                    }
                }

                if (response.data["shared"] != {}) {
                    let ftype = "shared";
                    let share_data = response.data["shared"];
                    for (let i = 0; i < share_data.length; i++) {
                        let ind = "shared" + String(i);
                        if (share_data[i] != {}) {
                            let share_row_file = share_data[i];
                            addFile(
                                share_row_file["sender"],
                                share_row_file["recipient"],
                                share_row_file["filename"],
                                share_row_file["fileurl"],
                                ftype,
                                ind
                            );
                        }
                    }
                }

                if (
                    response.data["shared"] == {} &&
                    response.data["own"] == {}
                ) {
                    cardgrid.style = "display: none;";
                    displayempty.style = "display: flex;";
                }
            } else {
                location.href = response.data["route"];
            }
        });
};

const homeowndownload = (event) => {
    let sender = event.target;
    let own_id = sender.id;
    let fn = own_id + "_filename";
    let fu = own_id + "_fileurl";

    let own_filename = document.getElementById(fn);
    let own_fileurl = document.getElementById(fu);

    if (own_filename) {
        let own_anchor = document.createElement("a");
        own_anchor.style = "display:none;";
        own_anchor.setAttribute("download", own_filename.textContent);
        own_anchor.setAttribute("href", own_fileurl.textContent);
        sender.appendChild(own_anchor);
        own_anchor.click();
        sender.removeChild(own_anchor);
    }
};
const homefiledownload = (event) => {
    let share_element = event.target;
    let shareid = share_element.id;
    let sender_id = shareid + "_sender";
    let recipient_id = shareid + "_recipient";
    let filename_id = shareid + "_filename";
    let fileurl_id = shareid + "_fileurl";

    let sender = document.getElementById(sender_id);
    let recipient = document.getElementById(recipient_id);
    let filename = document.getElementById(filename_id);
    let fileurl = document.getElementById(fileurl_id);

    if (filename) {
        let temp_anchor = document.createElement("a");
        temp_anchor.style = "display:none;";
        let fn_name = filename.textContent;
        let fn_url = fileurl.textContent;
        temp_anchor.setAttribute("download", fn_name);
        temp_anchor.setAttribute("href", fn_url);
        sender.appendChild(temp_anchor);
        temp_anchor.click();
        sender.removeChild(temp_anchor);
        var confimdown = confirm("Download file?");
        if(confimdown) {
            console.log('Downloading...');
        }
        axios
            .post(
                "/downloadupdate",
                {
                    sender: sender.textContent,
                    recipient: recipient.textContent,
                    filename: filename.textContent,
                    fileurl: fileurl.textContent,
                    isdownloaded: "True",
                },
                {
                    headers: {
                        "content-type": "application/json",
                    },
                }
            )
            .then((response) => {
                if (response.data.statusCode == 200) {
                    location.href = "/home";
                }
            })
            .catch((error) => {
                console.log("Error updating DB!");
            });
    }
};

const showUploadModal = () => {
    let modal = document.getElementById("uploadModal");
    let homecontent = document.getElementById("mainContent");
    modal.style.display = "block";
    homecontent.style.visibility = "hidden";
};

const onModalClose = () => {
    let modal = document.getElementById("uploadModal");
    let homecontent = document.getElementById("mainContent");
    modal.style.display = "none";
    location.reload(true);
    homecontent.style.visibility = "visible";
};

const validateEmail = (email) => {
    var validRegex =
        /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if (email.match(validRegex)) {
        return true;
    } else {
        return false;
    }
};

const addEmail = () => {
    let emailtags = document.getElementById("emailTags");
    let emailinput = document.getElementById("emailInput");

    let emailTagCount = emailtags.childElementCount;

    if (emailTagCount <= 0) {
        emailtags.style.display = "none";
    }

    if (emailTagCount < 5) {
        let emailText = emailinput.value;
        if (validateEmail(emailText)) {
            let newTag = document.createElement("span");
            newTag.className = "emailTag";
            newTag.innerText = emailText;
            newTag.id = "emailTag_" + String(emailTagCount + 1);
            let newTagIcon = document.createElement("i");
            newTagIcon.id = "icon-" + newTag.id;
            newTagIcon.className = "bx bxs-x-circle";
            newTagIcon.setAttribute("onclick", "deleteEmailTag(this.id);");
            newTag.appendChild(newTagIcon);
            if (emailTagCount <= 0) {
                emailtags.style.display = "flex";
            }
            emailtags.appendChild(newTag);
        }
    }

    emailinput.value = "";
};

const deleteEmailTag = (childId) => {
    let emailtags = document.getElementById("emailTags");
    let iconTag = document.getElementById(childId);
    let emailTag = iconTag.parentElement;
    emailtags.removeChild(emailTag);

    if (emailtags.childElementCount <= 0) {
        emailtags.style.display = "none";
    }
};

const onModalFormSubmit = () => {
    let emailinput = document.getElementById("emailInput");
    let emailTags = document.getElementById("emailTags");
    let fileInput = document.getElementById("fileUpload");

    let emails = [];
    for (let i = 0; i < emailTags.childElementCount; i++) {
        emails.push(emailTags.children[i].innerText);
    }

    emailinput.value = emails.join(",");

    let modalform = document.getElementById("modalForm");

    axios
        .post(
            "/upload",
            {
                user_sessionid: sessionStorage.getItem("user_sessionID"),
                emaillist: emailinput.value,
                fileupload: fileInput.files,
            },
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            }
        )
        .then((res) => {
            if (res.status == 200) {
                if (res.data.isUploaded == "true") {
                    alert("File uploaded successfully!");
                } else {
                    alert("File Upload Failed! Try Again later");
                }
                modalform.reset();
                location.href = res.data.route_to;
            } else {
                alert("File Upload Failed! Try Again later");
                modalform.reset();
                location.href = "/signin";
            }
        });
};

const checkExtension = (namefile) => {
    let fileExtArray = [
        "doc",
        "html",
        "css",
        "js",
        "json",
        "md",
        "txt",
        "png",
        "jpg",
        "gif",
        "pdf",
        "zip",
    ];
    let fileExt = namefile.split(".")[1];
    let fiClass = fileExtArray.includes(fileExt)
        ? "bx bxs-file" + "-" + fileExt
        : "bx bxs-file";
    return fiClass;
};

const updateThumbnail = (uploadAreaElement, file) => {
    let thumbnailElement = uploadAreaElement.querySelector(
        ".inputFileUpload__thumb"
    );

    if (
        uploadAreaElement.querySelector(".uploadInst") ||
        uploadAreaElement.querySelector(".uploadIcon")
    ) {
        uploadAreaElement.querySelector(".uploadInst").remove();
        uploadAreaElement.querySelector(".uploadIcon").remove();
    }
    if (!thumbnailElement) {
        let thumbnailElement = document.createElement("div");
        let filename = document.createElement("p");
        let fileIcon = document.createElement("i");

        let fiClass = checkExtension(file.name);

        fileIcon.className = fiClass;
        fileIcon.style =
            "font-size: 50px; background: transparent; color: #11beed; box-shadow:none; transform: none;";

        filename.innerText = file.name;
        filename.className = "uploadSelectp";
        filename.id = "fileUpID";
        filename.style = "font-size: 30px; color: #11beed;";

        thumbnailElement.style.background = "transparent";
        thumbnailElement.appendChild(fileIcon);
        thumbnailElement.appendChild(filename);
        thumbnailElement.classList.add("inputFileUpload__thumb");
        uploadAreaElement.appendChild(thumbnailElement);
    } else {
        let thumbnailElement = document.getElementsByClassName(
            "inputFileUpload__thumb"
        )[0];
        let fileuploaded = document.getElementById("fileUpID");
        fileuploaded.innerText = file.name;

        let fileExtArray = [
            "doc",
            "html",
            "css",
            "js",
            "json",
            "md",
            "txt",
            "png",
            "jpg",
            "gif",
            "pdf",
            "zip",
        ];
        let fileExt = file.name.split(".")[1];
        let fiClass = fileExtArray.includes(fileExt)
            ? "bx bxs-file" + "-" + fileExt
            : "bx bxs-file";
        thumbnailElement.children[0].className = fiClass;
    }
};

const downloadFile = () => {
    let sender = document.getElementById("downloadSender");
    let recipient = document.getElementById("downloadRecipient");
    let filename = document.getElementById("downloadFileName");
    let fileurl = document.getElementById("downloadFileURL");

    if (filename) {
        let temp_anchor = document.createElement("a");
        temp_anchor.style = "display:none;";
        let download_name = filename.textContent;
        let download_link = fileurl.textContent;
        temp_anchor.setAttribute("download", download_name);
        temp_anchor.setAttribute("href", download_link);
        sender.appendChild(temp_anchor);
        temp_anchor.click();
        sender.removeChild(temp_anchor);
        let isdownloaded = confirm('File downloaded successfully?');
        if(isdownloaded){
            console.log('Downloaded!');
        }
        axios
            .post(
                "/downloadupdate",
                {
                    sender: sender.textContent,
                    recipient: recipient.textContent,
                    filename: filename.textContent,
                    fileurl: fileurl.textContent,
                    isdownloaded: "True",
                },
                {
                    headers: {
                        "content-type": "application/json",
                    },
                }
            )
            .then((response) => {
                if (response.data.statusCode == 200) {
                    location.href = "/";
                }
            })
            .catch((error) => {
                console.log("Error updating DB!");
            });
    }
};

const logout = () => {
    sessionStorage.removeItem("user");
    sessionStorage.removeItem("user_sessionID");

    window.history.pushState(null, null, window.location.href);
    window.onpopstate = function () {
        history.go(1);
    };

    location.href = "/logout";
};
