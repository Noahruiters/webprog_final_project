document.addEventListener('DOMContentLoaded',function(){
    const questions = document.querySelectorAll('.question');
    const nextButton = document.getElementById('next_button');
    const submitButton = document.getElementById('submit_button');
    let currentQuestionIndex = 0;

    nextButton.onclick(function(){
        const currentQuestion=questions[currentQuestionIndex];
        if (input && input.value.trim() === '') {
            alert('Please answer the question before proceeding.');
            return;
        }

        currentQuestion.classList.remove('active');
        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            questions[currentQuestionIndex].classList.add('active');
        }

        if (currentQuestionIndex === questions.length - 1) {
            nextButton.style.display = 'none';
            submitButton.style.display = 'inline-block';
        }

    })










})