"use strict";

document.addEventListener("DOMContentLoaded", function () {
    // ------------------------------------------------------- //
    // Transition Placeholders
    // ------------------------------------------------------ //
    let materialInputs = document.querySelectorAll("input.input-material");
    let materialLabel = document.querySelectorAll("label.label-material");

    // activate labels for prefilled values
    let filledMaterialInputs = Array.from(materialInputs).filter(function (input) {
        return input.value !== "";
    });
    filledMaterialInputs.forEach((input) => input.parentElement.lastElementChild.setAttribute("class", "label-material active"));

    // move label on focus
    materialInputs.forEach((input) => {
        input.addEventListener("focus", function () {
            input.parentElement.lastElementChild.setAttribute("class", "label-material active");
        });
    });

    // remove/keep label on blur
    materialInputs.forEach((input) => {
        input.addEventListener("blur", function () {
            if (input.value !== "") {
                input.parentElement.lastElementChild.setAttribute("class", "label-material active");
            } else {
                input.parentElement.lastElementChild.setAttribute("class", "label-material");
            }
        });
    });

    // ------------------------------------------------------- //
    // Footer重製，因為sidebar展開、關閉會影響
    // ------------------------------------------------------ //
    let footer = document.querySelector("#footer");
    if (footer) {
        document.addEventListener("sidebarChanged", function () {
            adjustFooter();
        });
        window.addEventListener("resize", function () {
            adjustFooter();
        });
    }

    function adjustFooter() {
        var footerBlockHeight = document.querySelector("#footer").outerHeight;
        pageContent.style.paddingBottom = `${footerBlockHeight}px`;
    }

    // ------------------------------------------------------- //
    // Card Close
    // ------------------------------------------------------ //
    const closeCardBtn = document.querySelectorAll(".card-close a.remove");
    closeCardBtn.forEach((el) => {
        el.addEventListener("click", (e) => {
            e.preventDefault();
            el.closest(".card").style.opacity = "0";
            setTimeout(function () {
                el.closest(".card").classList.add("d-none");
            }, 300);
        });
    });

    // ------------------------------------------------------- //
    // Card Close dropdown
    // ------------------------------------------------------ //
    const cardSettingsToggle = document.querySelectorAll(".card-close .dropdown-toggle");
    cardSettingsToggle.forEach((el) => {
        el.addEventListener("click", () => {
            if (el.classList.contains("show")) {
                setTimeout(function () {
                    el.nextElementSibling.classList.add("is-visible");
                }, 100);
            }
        });
    });

    document.addEventListener("click", function (e) {
        cardSettingsToggle.forEach((el) => {
            if (e.target == el) {
                setTimeout(function () {
                    el.nextElementSibling.classList.add("is-visible");
                }, 100);
            } else {
                el.nextElementSibling.classList.remove("is-visible");
            }
        });
    });

    // ------------------------------------------------------- //
    // Tooltips init
    // ------------------------------------------------------ //
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ------------------------------------------------------- //
    // Sidebar縮小、恢復正常的按鈕
    // ------------------------------------------------------ //
    var sidebarToggler = document.querySelector(".sidebar-toggle");
    var sidebar = document.querySelector("#sidebar");
    var pageContent = document.querySelector(".page-content");
    var navBrand = document.querySelector(".navbar-brand");
    if (sidebarToggler) {
        sidebarToggler.addEventListener("click", function () {

            this.classList.toggle("active");
            navBrand.classList.toggle("active");

            sidebar.classList.toggle("shrinked");
            pageContent.classList.toggle("active");
            document.dispatchEvent(new Event("sidebarChanged"));
        });
    }
    // ------------------------------------------------------- //
    // Sidebar調整active位置
    // ------------------------------------------------------ //
    function handleSidebarUpdate(pathname = window.location.pathname) {
        if (pathname === "/") {
            const rootItem = document.getElementById("index");
            rootItem?.classList.add("active");
            return;
        }

        const [first, second] = pathname.split("/").slice(1);
        const parentItem = document.getElementById(first);
        if (!parentItem) return;

        parentItem.classList.add("active");

        const subList = parentItem.querySelector(".collapse.list-unstyled");
        subList?.classList.add("show");

        const subItem = document.getElementById(second);
        subItem?.classList.add("active");
    }
    handleSidebarUpdate();

    // 服務於底下功能的function，停用
    function bsValidationBehavior(errorInputs, form) {
        function watchError() {
            errorInputs.forEach((input) => {
                if (input.classList.contains("js-validate-error-field")) {
                    input.classList.add("is-invalid");
                    input.classList.remove("is-valid");
                } else {
                    input.classList.remove("is-invalid");
                    input.classList.add("is-valid");
                }
            });
        }
        watchError();
    }

    // ------------------------------------------------------- //
    // Login Form Validation
    // ------------------------------------------------------ //
    // let loginForm = document.querySelector(".login-form");
    // if (loginForm) {
    //     new window.JustValidate(".login-form", {
    //         rules: {
    //             loginUsername: {
    //                 required: true,
    //                 email: true,
    //             },
    //             loginPassword: {
    //                 required: true,
    //             },
    //         },
    //         messages: {
    //             loginUsername: "Please enter a valid email",
    //             loginPassword: "Please enter your password",
    //         },
    //         invalidFormCallback: function () {
    //             let errorInputs = document.querySelectorAll(".login-form input[required]");
    //             bsValidationBehavior(errorInputs, loginForm);
    //             loginForm.addEventListener("keyup", () => bsValidationBehavior(errorInputs, loginForm));
    //         },
    //     });
    // }

    // ------------------------------------------------------- //
    // 為註冊表單提供驗證功能，確保用戶輸入有效的資料
    // ------------------------------------------------------ //
    // let registerForm = document.querySelector(".register-form");
    // if (registerForm) {
    //     new window.JustValidate(".register-form", {
    //         rules: {
    //             registerUsername: {
    //                 required: true,
    //             },
    //             registerEmail: {
    //                 required: true,
    //                 email: true,
    //             },
    //             registerPassword: {
    //                 required: true,
    //             },
    //             registerAgree: {
    //                 required: true,
    //             },
    //         },
    //         messages: {
    //             registerUsername: "Please enter your username",
    //             registerEmail: "Please enter a valid email address",
    //             registerPassword: "Please enter your password",
    //             registerAgree: "Your agreement is required",
    //         },
    //         invalidFormCallback: function () {
    //             let errorInputs = document.querySelectorAll(".register-form input[required]");
    //             bsValidationBehavior(errorInputs, registerForm);
    //             registerForm.addEventListener("keyup", () => bsValidationBehavior(errorInputs, registerForm));
    //             registerForm.addEventListener("change", () => bsValidationBehavior(errorInputs, registerForm));
    //         },
    //     });
    // }

    // ------------------------------------------------------- //
    // Profile page choices
    // ------------------------------------------------------ //
    function injectClassess(x) {
        let pickerCustomClass = x.dataset.customclass;
        let pickerSevClasses = pickerCustomClass.split(" ");
        x.parentElement.classList.add.apply(x.parentElement.classList, pickerSevClasses);
    }

    const profileCountryChoices = document.querySelector(".profile-country-choices");
    if (profileCountryChoices) {
        const countryChoices = new Choices(profileCountryChoices, {
            searchEnabled: false,
            placeholder: false,
            callbackOnInit: () => injectClassess(profileCountryChoices),
        });
    }

    // ------------------------------------------------------- //
    // 使用 Masonry 排版插件對帶有圖片的元素進行網格布局並確保圖片加載完成後重新計算布局
    // ------------------------------------------------------ //
    const masonryGrid = document.querySelector(".msnry-grid");
    if (masonryGrid) {
        var msnry = new Masonry(masonryGrid, {
            percentPosition: true,
        });
        imagesLoaded(masonryGrid).on("progress", function () {
            msnry.layout();
        });
    }
});
