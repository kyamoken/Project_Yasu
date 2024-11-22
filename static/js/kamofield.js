(async () => {
    // ラベル要素の横方向の余白設定
    const labelPaddingX = 20;

    // ルールの設定
    const globalRules = {
        required: (value) => !!value,

        // 比較演算
        equals: (value, text) => value === text,
        not: (value, text) => value !== text,

        min: (value, min) => value.length >= min,
        max: (value, max) => value.length <= max,
        between: (value, min, max) => value.length >= min && value.length <= max,
        length: (value, length) => value.length === length,

        // 一般的なルール
        email: (value) => /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value),
        number: (value) => /^[0-9]+(\.[0-9]+)?$/.test(value),
        integer: (value) => /^[0-9]+$/.test(value),
        alpha: (value) => /^[a-zA-Z]+$/.test(value),
        in: (value, ...args) => args.includes(value),

        // 特殊ルール
        regex: (value, regex) => new RegExp(regex).test(value),
        equals_ref: (value, target) => value === findFieldElement(target)?.value,
    }



    ///////////////////////////////////////////////////////
    // 以下、ライブラリの初期化
    ///////////////////////////////////////////////////////

    function findFieldElement(queryOrElement, formElement = document) {
        if (!queryOrElement) {
            return null;
        }

        const container = queryOrElement instanceof HTMLElement
            ? queryOrElement
            : formElement.querySelector(queryOrElement);

        if (!container) {
            console.error(`指定された要素が見つかりませんでした。(${queryOrElement})`);
            return null;
        }

        if (container.tagName === 'INPUT' || container.tagName === 'TEXTAREA' || container.tagName === 'SELECT') {
            return container;
        }

        return container.querySelector('input, textarea, select');
    }

    const formElements = document.querySelectorAll('form, .kamoform') ?? [document];

    formElements.forEach((formElement) => {
        // ラベルの最大幅を取得
        const maxLabelWidth = Math.max(...Array.from(formElement.querySelectorAll('.kamofield .label span'), el => el.offsetWidth));

        formElement.addEventListener('submit', (event) => {
            event.preventDefault();
            const form = event.target;
            const fields = form.querySelectorAll('.kamofield');
            let isValid = true;
            let firstInvalidField = null;
            for (const field of fields) {
                validateField(field, true, true);
                if (field.classList.contains('is-invalid')) {
                    isValid = false;
                    if (!firstInvalidField) {
                        firstInvalidField = field;
                    }
                }
            }

            if (isValid) {
                form.submit();
            } else {
                firstInvalidField.querySelector('input, textarea, select').focus();
            }
        });　

        /**
        * ルールのメッセージ
        * @type {Object.<string, string[]>} キーにルール名、値に該当関数に渡す引数の配列
        */
        function parseRule(ruleText) {
            if (!ruleText) {
                return {};
            }

            const rules = ruleText.split(' ');
            const ruleObj = {};
            for (const rule of rules) {
                const [ruleName, ruleValue] = rule.split(':');
                const ruleArgs = ruleValue?.split(',') ?? [];
                ruleObj[ruleName] = ruleArgs;
            }

            return ruleObj;
        }

        function validateField(container, addInvalidClass = false, apply_required = false) {
            const inputEl = container.querySelector('input, textarea, select');
            const value = inputEl.value;
            const regex = container.getAttribute('data-regex');
            const issetRule = !!container.dataset.rule;

            const isFilled = inputEl.nodeName === 'SELECT' ? !inputEl[inputEl.selectedIndex]?.disabled : !!inputEl.value;


            // ルールが設定されている場合
            if (container.dataset.rule) {
                const rules = parseRule(container.dataset.rule);
                if (!isFilled) {
                    container.classList.remove('is-valid');
                    container.classList.remove('is-invalid');
                    if (apply_required && rules.required) {
                        container.classList.add('is-invalid');
                    }
                    return;
                }

                let isValid = true;
                for (const [ruleName, ruleArgs] of Object.entries(rules)) {
                    const ruleFunc = globalRules[ruleName];
                    if (ruleFunc) {
                        const result = ruleFunc(value, ...ruleArgs);
                        if (!result) {
                            isValid = false;
                            break;
                        }
                    } else {
                        console.error(`存在しないルールが指定されました。(${ruleName})`);
                    }
                }

                if (isValid) {
                    container.classList.add('is-valid');
                    container.classList.remove('is-invalid');
                } else {
                    container.classList.remove('is-valid');
                    if (addInvalidClass) {
                        container.classList.add('is-invalid');
                    }
                }

                return;
            }

            if (value) {
                container.classList.add('is-valid');
            } else {
                container.classList.remove('is-valid');
            }
        }

        formElement.querySelectorAll('.kamofield')?.forEach((element) => {
            // ラベルにアイコンを追加
            const iconSize = '18px';
            const checkCircleIconHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="validation-icon valid" width="' + iconSize + '" height="' + iconSize + '" viewBox="0 -960 960 960"><path d="m424-296 282-282-56-56-226 226-114-114-56 56 170 170Zm56 216q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg>';
            const errorIconHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="validation-icon invalid" width="' + iconSize + '" height="' + iconSize + '" viewBox="0 -960 960 960"><path d="M480-280q17 0 28.5-11.5T520-320q0-17-11.5-28.5T480-360q-17 0-28.5 11.5T440-320q0 17 11.5 28.5T480-280Zm-40-160h80v-240h-80v240Zm40 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg>';
            element.querySelector('.label').insertAdjacentHTML('beforeend', checkCircleIconHTML + errorIconHTML);

            const rules = parseRule(element.dataset.rule);
            if (rules.equals_ref) {
                const target = rules.equals_ref[0];
                const targetEl = findFieldElement(target, formElement);
                if (targetEl) {
                    targetEl.addEventListener('input', () => {
                        validateField(element);
                    });
                }
            }

            // リスナーを設定
            const inputEl = element.querySelector('input, textarea, select');
            const isSelectElement = inputEl.nodeName === 'SELECT';

            inputEl.addEventListener('input', (event) => {
                const target = event.target;

                if (element.dataset.rule || element.dataset.rule === '') {
                    validateField(target.parentNode);
                } else {
                    if (!target.value) {
                        target.parentNode.classList.remove('is-valid');
                        target.parentNode.classList.remove('is-invalid');
                    }
                }
            });

            inputEl.addEventListener('focus', () => {
                element.classList.add('focused');
                const labelEl = element.querySelector('.label');
                const labelTextEl = labelEl.firstElementChild;
                const labelTextWidth = labelTextEl.offsetWidth;
                const inputEl = element.querySelector('input, textarea, select');

                labelEl.style.width = `${maxLabelWidth + labelPaddingX * 2}px`;
                inputEl.style.left = `${maxLabelWidth + labelPaddingX * 2}px`;
                inputEl.style.width = `calc(100% - ${maxLabelWidth + labelPaddingX * 2}px)`;

            });

            if (isSelectElement) {
                inputEl.addEventListener('change', (event) => {
                    const target = event.target;
                    validateField(element, true);
                });
                inputEl.addEventListener('blur', (event) => {
                    const target = event.target;
                    element.classList.remove('focused');
                    if (target[target.selectedIndex]?.disabled) {
                        const labelEl = element.querySelector('.label');
                        const inputEl = element.querySelector('input, textarea, select');
                        labelEl.style.width = '100%';
                        element.classList.remove('filled');
                    } else {
                        element.classList.add('filled');
                    }

                    // validation
                    validateField(element, true, false);
                });
            } else {
                inputEl.addEventListener('blur', (event) => {
                    const target = event.target;
                    element.classList.remove('focused');
                    if (!target.value) {
                        const labelEl = element.querySelector('.label');
                        const inputEl = element.querySelector('input, textarea, select');
                        labelEl.style.width = '100%';
                    }

                    if (target.value) {
                        element.classList.add('filled');
                    } else {
                        element.classList.remove('filled');
                    }

                    // validation
                    validateField(element, true, false);
                });
            }

            // 初期化
            validateField(element, true, false);

            const isFilled = inputEl.nodeName === 'SELECT' ? !inputEl[inputEl.selectedIndex]?.disabled : !!inputEl.value;
            if (isFilled) {
                element.classList.add('filled');

                const labelEl = element.querySelector('.label');
                const inputEl = element.querySelector('input, textarea, select');
                labelEl.style.width = `${maxLabelWidth + labelPaddingX * 2}px`;
                inputEl.style.left = `${maxLabelWidth + labelPaddingX * 2}px`;
                inputEl.style.width = `calc(100% - ${maxLabelWidth + labelPaddingX * 2}px)`;
            }

            setTimeout(() => {
                element.dataset.ready = '';
            }, 200)
        })
    });
})();

// テキストエリアの自動リサイズ
document.querySelectorAll('textarea.autosize').forEach((element) => {
    element.style.height = element.scrollHeight + 'px';
    element.addEventListener('input', () => {
        element.style.height = 'auto';
        element.style.height = element.scrollHeight + 'px';
    });
});
