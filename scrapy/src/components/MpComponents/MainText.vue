<template>
    <v-container>
      <div class="typewriter">
        <div class="typewriter-text">
          <div v-for="(line, index) in lines" :key="index">{{ line }}</div>
        </div>
        <img src="@/assets/maingif2.gif" alt="Main GIF" />
      </div>
    </v-container>
  </template>
  
  <script>
  export default {
  data() {
    return {
      phrases: [
        'BUY AND SELL WITH PEOPLE WHO SHARE YOUR PASSION',
        'GET INSPIRED, GET CREATIVE, GET CRAFTING',
        'SCRAP ISN’T WASTE, IT’S YOUR NEXT PROJECT',
      ],
      lines: [], // Array to hold each completed line
      currentPhraseIndex: 0,
      currentCharIndex: 0,
      isDeleting: false,
      typingSpeed: 50,
      deletingSpeed: 30,
      pauseDuration: 1500,
    };
  },
  mounted() {
    this.typeText();
  },
  methods: {
    typeText() {
      const currentPhrase = this.phrases[this.currentPhraseIndex];
      const currentLine = this.lines[this.lines.length - 1] || '';

      if (!this.isDeleting) {
        if (this.currentCharIndex < currentPhrase.length) {
          if (this.currentCharIndex === 0) {
            this.lines.push(''); // Start a new line
          }
          this.lines[this.lines.length - 1] = currentLine + currentPhrase[this.currentCharIndex];
          this.currentCharIndex++;
          setTimeout(this.typeText, this.typingSpeed);
        } else {
          setTimeout(() => {
            this.isDeleting = true;
            this.typeText();
          }, this.pauseDuration);
        }
      } else {
        if (this.currentCharIndex > 0) {
          this.lines[this.lines.length - 1] = currentLine.slice(0, -1);
          this.currentCharIndex--;
          setTimeout(this.typeText, this.deletingSpeed);
        } else {
          this.lines.pop(); // Remove the line when fully deleted
          this.isDeleting = false;
          this.currentPhraseIndex = (this.currentPhraseIndex + 1) % this.phrases.length;
          setTimeout(this.typeText, this.typingSpeed);
        }
      }
    },
  },
};

  </script>
  
  <style scoped>
.typewriter {
  display: flex;
  /* flex-direction: column;  */
  justify-content: center;
  align-items: center;
  height: 30vh;
  position: relative;
  top: 10vh;
}

.typewriter-text {
  font-size: 5vw;
  color: lightgreen;
  text-align:start ;
  font-family: "Concert One", serif;
  line-height: 1; /* Consistent spacing between lines */
  width: 90vw;
  /* white-space: nowrap; Prevents text wrapping */
  overflow: hidden;
}


@media(max-width:425px){
  .typewriter-text{
    display: hidden;
  }
}
  </style>
  