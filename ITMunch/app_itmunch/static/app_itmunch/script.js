document.addEventListener('DOMContentLoaded',function(){

    console.log("script loaded");

    const questions = document.querySelectorAll('.question');
    const nextButton = document.querySelector('#button_next');
    const submitButton = document.querySelector('#button_submit');
    const form = document.querySelector('form');
    let currentQuestionIndex = 0;


    nextButton.onclick=function(){
        console.log("button clicked");
        const currentQuestion=questions[currentQuestionIndex];
        const input = currentQuestion.querySelector('input, select, textarea'); // Select input field of the current question
        //if the question is not answered, display an alert message
        if (input && input.value.trim() === '') {
            alert('Please answer the question');
            return;
        }

        //change the active question to the next field
        currentQuestion.classList.remove('active');
        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            questions[currentQuestionIndex].classList.add('active');
        }

        //for the last question, make the button submit active, and next inactive
        if (currentQuestionIndex === questions.length - 1) {
            nextButton.style.display = 'none';
            submitButton.style.display = 'inline-block';
            submitButton.onclick=function(){
                form.submit(); // submit the form
            };
        }
    }
})
