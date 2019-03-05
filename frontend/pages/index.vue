<template>
  <div>
    <input type="text" v-model="inputMessage">
    <button @click="submit()">submit</button>
    <p v-for="message in messages" :key="message.id">
      {{ message.sender }}「{{ message.contents }}」<br>
      <small>{{ message.timestamp }} {{ message.blockhash }}</small>
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { EasyClientForBrowser } from '@uniqys/easy-client'

interface Message {
  id: number
  sender: string
  contents: string
  timestamp: string
  blockhash: string
}

@Component({
})
export default class Home extends Vue {
  public messages: Message[] = [];
  public inputMessage: string = "";
  public client!: EasyClientForBrowser;
  async mounted() {
    this.client = new EasyClientForBrowser('http://localhost:8080')
    console.log("created")
    await this.update()
  }
  async update() {
    const { data } = await this.client.get('/api/message');
    const { messages } = data as { messages: Message[] };
    this.messages = messages
  }
  async submit() {
    await this.client.post(
      '/api/message',
      { contents: this.inputMessage },
      { sign: true })
    await this.update()
  }
}
</script>