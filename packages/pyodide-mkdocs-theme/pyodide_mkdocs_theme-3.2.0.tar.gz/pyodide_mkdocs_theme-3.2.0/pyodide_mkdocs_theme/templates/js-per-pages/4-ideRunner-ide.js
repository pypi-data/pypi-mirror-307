/*
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
*/


ace.require("ace/ext/language_tools");



class IdeStorageAndZipManager extends TerminalRunner {


  /**Process to "re-initiate" the internal state of the IDE (useful for testing) */
  constructor(editorId){
    super(editorId)
    this.storage = null
    this.getStorage()
  }


  _extractWhateverLocalStorageVersion(editorId){
    const  extractForThis = editorId==this.id
    return getIdeDataFromStorage(editorId, extractForThis ? this : null)
  }


  getStorage(){
    let [storage, outdated] = this._extractWhateverLocalStorageVersion(this.id)
    this.storage = storage

    // Enforce update of internal values:
    if( outdated || this.storage.name!=this.pyName || this.storage.zip!=this.export ){
      this.setStorage({name: this.pyName, zip:  this.export})
    }
  }


  setStorage(changes){
    if(changes){
      for(const k in changes) this.storage[k] = changes[k]
    }
    localStorage.setItem(this.id, JSON.stringify(this.storage))
  }


  announceCodeChangeBasedOnSrcHash(){
    if(this.storage.hash != this.srcHash){
      this.terminalEcho(CONFIG.lang.refresh.msg)
    }
  }


  /**Automatically gives the focus to the ACE editor with the given id.
   * */
  focusEditor(){
    this.editor.focus()
  }



  buildZipExportsToolsAndCbk(jBtn){

    // Add drag&Drop behavior for zip archives:
    jBtn.on("dragenter dragstart dragend dragleave dragover drag", e=>e.preventDefault())

    // Doesn't work using jQuery... (again... x/ ):
    jBtn[0].addEventListener('drop', this.dropArchiveFactory(
      this.lockedRunnerWithBigFailWarningFactory(
        CONFIG.runningMode.zipImport,
        this.setupRuntimeZip,
        this.dropArchive,
        this.teardownRuntimeZip,
        true,
      )
    ))

    return this.lockedRunnerWithBigFailWarningFactory(
      CONFIG.runningMode.zipExport,
      this.setupRuntimeZip,
      this.zipExport,
      this.teardownRuntimeZip,
    )
  }


  async setupRuntimeZip(){
    this.terminal.pause()           // Deactivate user actions in the terminal until resumed
    this.terminal.clear()           // To do AFTER pausing...
    const [runtime,] = await this._baseSetupRuntime()
    return runtime
  }

  async teardownRuntimeZip(runtime){
    this.terminal.resume()
    await this._baseTeardownRuntime(runtime)
  }




  _getDataForExportableIdeInPage(){
    const toArchive = []
    const ideThis   = this

    $(`[id^=editor_]`).each(function(){
      if(localStorage.getItem(this.id)===null){
        return    // should never happen... But just in case...
      }
      const [data,] = ideThis._extractWhateverLocalStorageVersion(this.id)
      data.id = this.id
      if(data.zip){             // Exportable
        toArchive.push(data)
      }
    })
    return toArchive
  }


  _buildZipNameFirstChunks(){
    const zipChunks = []

    if(CONFIG.exportZipPrefix){
      zipChunks.push(CONFIG.exportZipPrefix)
    }
    if(CONFIG.exportZipWithNames){
      let names = ""
      while(!names){
        names = window.prompt(CONFIG.lang.zipAskForNames.msg)
      }
      zipChunks.push(names)
    }
    return zipChunks
  }


  async zipExport(_runtime){
    this.terminalEcho('Generate zip for '+location.href)

    const toArchive = this._getDataForExportableIdeInPage()
    const zipChunks = this._buildZipNameFirstChunks()
    const code      = this._buildZipExportPythonCode(toArchive, zipChunks)
    pyodide.runPython(code)
    this.focusEditor()
  }


  _buildZipExportPythonCode(toArchive, zipChunks){
    const pyJson = JSON.stringify(toArchive).replace(/\\/g, '\\\\')
    return `
@__builtins__.auto_run
def _hack_build_zip():

    import shutil, json
    from pathlib import Path
    from itertools import count

    def unique_name(p:Path):
        while p.exists():
            p = p.with_name(f"{ p.stem }_{ p.suffix }")
        return p

    dirname = unique_name(Path('tmp_zip'))
    dirname.mkdir()

    url    = ${ JSON.stringify(location.href) }
    origin = ${ JSON.stringify(location.origin) }
    chunks = ${ JSON.stringify(zipChunks) }

    # Always make sure the url part of the filename is not empty:
    zip_url = url[len(origin):].strip('/').replace('/','_').replace('.','_') or 'home'
    chunks.append(zip_url)

    zip_name = unique_name( Path( '-'.join(chunks) + '.zip') )

    data = json.loads("""${ pyJson }""")
    for ide in data:
        name = dirname / (ide['id'] + '${ CONFIG.ZIP.pySep }' + ide['name'])
        name.write_text(ide['code'], encoding="utf-8")

    shutil.make_archive(zip_name.with_suffix(''), 'zip', dirname)

    pyodide_downloader(
        zip_name.read_bytes(),
        zip_name.name,
        "application/zip"   # "application/x-zip-compressed" on Windaube...?
                            # => no need (probably because in WASM)
    )
    shutil.rmtree(dirname)
    zip_name.unlink()
`
  }



  dropArchiveFactory(asyncRuntimeConsumer){
    return async ev=>{
      ev.preventDefault()
      CONFIG.loadIdeContent = this.loadIdeContent.bind(this)
      await asyncRuntimeConsumer(ev)
    }
  }


  async dropArchive(ev){
    // https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop
    // https://stackoverflow.com/questions/43180248/firefox-ondrop-event-datatransfer-is-null-after-update-to-version-52

    const useItems = Boolean(ev.dataTransfer.items)
    const files = [...ev.dataTransfer[ useItems?'items':'files' ]]

    if(files.length!=1){
      this.giveFeedback("Cannot Import multiple archives.")
      return
    }

    files.forEach((itemOrFile) => {
      if(useItems && itemOrFile.kind !== "file"){
        // If dropped items aren't files, reject them
        return
      }
      this.getZipContentAsBytes( useItems ? itemOrFile.getAsFile():itemOrFile)
    })
  }


  getZipContentAsBytes(file){
    const reader = new FileReader();

    reader.onload = function(event){
      const bytesArr = event.target.result
      pyodide.unpackArchive(bytesArr, "zip", {extractDir: CONFIG.ZIP.tmpZipDir})
      pyodide.runPython(`
@__builtins__.auto_run
def _hack_zip_loading():
    from pathlib import Path
    import js
    loadIdeContent = js.config().loadIdeContent

    tmp_dir = Path('${ CONFIG.ZIP.tmpZipDir }')
    for py in tmp_dir.iterdir():
        content = py.read_text(encoding='utf-8')
        loadIdeContent(py.name, content)
        py.unlink()
    tmp_dir.rmdir()
`)
    }
    reader.readAsArrayBuffer(file)
  }


  loadIdeContent(pyName, code){
    const i        = pyName.indexOf(CONFIG.ZIP.pySep)
    const editorId = pyName.slice(0, i)
    const name     = pyName.slice(i+1)
    const jIde     = $('#'+editorId)

    if(!jIde[0]){
      this.giveFeedback(
        `Couldn't find the IDE #${editorId} in the page (associated python name: ${ name })`
      )
    }else{
      ace.edit(editorId).getSession().setValue(code);
      // No save/localStorage handling at this point (I don't have the IdeRunner object in hand :p )
      this.giveFeedback(`Loaded ${ editorId }${ CONFIG.ZIP.pySep }${ name }.`, "none")
    }
  }
}

















class _IdeEditorHandler extends IdeStorageAndZipManager {

  constructor(editorId){
    super(editorId)

    this.termId        = "term_" + editorId
    this.commentIdH    = "#comment_" + editorId
    this.globalIdH     = "#global_" + editorId
    this.inputIdH      = "#input_" + editorId
    this.counterH      = "#compteur_" + editorId
    this.delay         = 200            // Delay to wait after clearing the terminal content, (user actions)
    this.editor        = null           // ACE object
    this.resizedTerm   = !this.isVert   // Flag to know if the terminal size dimensions have already been enforced or not.
    this.getCodeToTest = ()=>this.editor.getSession().getValue()
    this._init()
  }


  /**Process to "re-initiate" the internal state of the IDE (useful for testing) */
  _init(){
    super._init()
    this.hiddenDivContent = true
    this.srcAttemptsLeft  = this.attemptsLeft
  }



  // @Override
  build(){

    // Create and define this.editor + fill code content + define all needed listeners:
    this.setupAceEditor()
    this.bindIdeButtons()

    super.build(this.termId)

    // Once the terminal is properly built, check for outdated IDE content and fix the "wrong"
    // behaviors of the terminal.
    this.announceCodeChangeBasedOnSrcHash()
    this.fixTerminalBehaviors()
  }


  fixTerminalBehaviors(){
    // Add the resize listener (because of the intermediate div wrappers, IDE's terminal
    // will not resize automatically):
    window.addEventListener(
      'resize',
      _.throttle( this.terminalAutoWidthOnResize.bind(this), 50, {leading:false, trailing:true} )
    )

    if(this.isVert){
      // Resize on next tick, once the editor has been filled with code (automatic height):
      setTimeout(_=>this.resizeVerticalTerm(false))

      // In case an IDEv is "tabbed", it won't resize properly because the editor is not handled
      // the same way, so put in place a "run once" click event, to resize it when the user
      // clicks on the _parent_ div (because the terminal itself is 0px high! XD )
      this.addEventToRunOnce(this.terminal.parent(), _=>this.resizeVerticalTerm())
    }
  }


  resizeVerticalTerm(mark=true){
    if(!this.isVert || this.resizedTerm) return;
    jsLogger("[CheckPoint] - Handle terminal window size")

    const divHeight = $('#'+this.id).css('height')
    const term_div = $(`${ this.globalIdH } .term_editor_v`)
    term_div.css("height", divHeight)
    this.resizedTerm = mark
  }



  /**Create and setup the ACE editor for the current Ide instance.
   * */
  setupAceEditor() {

    // https://github.com/ajaxorg/ace/blob/092b70c9e35f1b7aeb927925d89cb0264480d409/lib/ace/autocomplete.js#L545
    const options = {
        autoScrollEditorIntoView: false,
        copyWithEmptySelection:   true,               // active alt+flèches pour déplacer une ligne, aussi
        enableBasicAutocompletion:true,
        enableLiveAutocompletion: false,
        enableSnippets:           true,
        tabSize:                  4,
        useSoftTabs:              true,               // Spaces instead of tabs
        navigateWithinSoftTabs:   false,              // this is _fucking_ actually "Atomic Soft Tabs"...
        printMargin:              false,              // hide ugly margins...
        maxLines:                 this.maxIdeLines,
        minLines:                 this.minIdeLines,
        mode:                     "ace/mode/python",
        theme:                    getTheme(),
        fontFamily:               CONFIG.editorFontFamily,   // Fix apple troubles...
    }

    const editor = this.editor = ace.edit(this.id, options);
    if(CONFIG._devMode) CONFIG.editors[this.id] = editor

    editor.commands.bindKey(
        { win: "Ctrl-Space", mac: "Cmd-Space" }, "startAutocomplete"
    )
    editor.commands.addCommand({
        name: "commentTests",
        bindKey: { win: "Ctrl-I", mac: "Cmd-I" },
        exec: this.toggleComments.bind(this),
    })
    editor.commands.addCommand({
        name: "runPublicTests",
        bindKey: { win: "Ctrl-S", mac: "Cmd-S" },
        exec: this.playFactory(),
    })
    if(this.hasCheckBtn){
        editor.commands.addCommand({
        name: "runValidationTests",
        bindKey: { win: "Ctrl-Enter", mac: "Cmd-Enter" },
        exec: this.validateFactory(),
      })
    }

    // Content of the editor is saved every `CONFIG.ideKeyStrokesSave` keystrokes:
    let nChange = 0;
    this.editor.addEventListener("input", _=>{
        if(nChange++ >= CONFIG.ideKeyStrokesSave){
          nChange=0
          this.save()
        }
    })

    // Try to restore a previous session, or extract default starting code:
    let exerciseCode = this.getStartCode(true)
    this.applyCodeToEditorAndSave(exerciseCode, false)
    this.editor.resize();
  }



  bindIdeButtons(){
    // Bind the ### "button":
    $(this.commentIdH).on("click", this.toggleComments.bind(this))


    // Bind all buttons below the IDE
    const ideThis = this
    $(this.globalIdH).find("button").each(function(){
      const btn  = $(this)
      const kind = btn.attr('btn_kind')
      let callback

      switch(kind){
        case 'play':      callback = ideThis.playFactory() ; break
        case 'check':     callback = ideThis.runner = ideThis.validateFactory()
                          ideThis.updateValidationBtnColor()
                          break

        case 'download':  callback = _=>ideThis.download() ; break
        case 'upload':    callback = _=>uploader( txt=>{
                                        ideThis.applyCodeToEditorAndSave(txt)
                                        ideThis.focusEditor()
                                      }) ; break

        case 'restart':   callback = _=>ideThis.restart() ; break
        case 'save':      callback = _=>{ideThis.save(); ideThis.focusEditor()} ; break
        case 'zip':       callback = ideThis.buildZipExportsToolsAndCbk(btn) ; break

        case 'corr_btn':  if(!CONFIG.inServe) return;
                          callback = ideThis.validateCorrFactory() ; break
        case 'show':      if(!CONFIG.inServe) return;
                          callback = ()=>ideThis.revealSolutionAndRems() ; break

        default:          throw new Error(`Y'should never get there, mate... (${ kind })`)
      }
      btn.on('click', callback)
    })
  }



  // @Override
  getTerminalBindings(){

    // Ensure the focus is given back to the terminal after an action triggered from it!
    const asyncTermFocus=(cbk)=>async e=>{
      await cbk(e)
      this.editor.blur()
      this.terminal.focus()
    }
    return ({
      ...super.getTerminalBindings(),
      'CTRL+I': asyncTermFocus(this.toggleComments.bind(this)),
      'CTRL+S': asyncTermFocus(this.playFactory()),
      ...(!this.hasCheckBtn ? {} : {'CTRL+ENTER': asyncTermFocus(this.validateFactory())} ),
    })
  }


  /**Add the `tests` section to the given code, joining them with the appropriated
   * string/comment if needed.
   * */
  _joinCodeAndPublicSections(userCode){
    const editorCode = [ userCode, this.publicTests ].filter(Boolean).join(CONFIG.lang.tests.msg)
    return editorCode
  }



  /**Build (or extract if allowed) the initial code to put in the editor.
   * */
  getStartCode(attemptLocalStorageExtraction=false){
    let exerciseCode = ""

    if(attemptLocalStorageExtraction){
      exerciseCode = this.storage.code
    }
    if(!exerciseCode){
      exerciseCode = this._joinCodeAndPublicSections(this.userContent)
    }

    // Enforce at least one empty line of code in the editor, so that the terminal prompt
    // is always visible for IDEv:
    exerciseCode = exerciseCode.replace(/\n+$/,'')
    if(!exerciseCode) exerciseCode = '\n'

    return exerciseCode+"\n"
  }


  /**Takes in the id string of an editor, or an ACE editor as first argument, and the
   * code string to apply to it, and:
   *      - set the editor content to that string
   *      - save the code to the localStorage
   * */
  applyCodeToEditorAndSave(exerciseCode, doSave=true){
    exerciseCode ||= ""
    // Not satisfying:
    // const nLF = this.minIdeLines-1 - exerciseCode.replace(/[^\n]+/g, '').length
    // if(nLF>0){
    //   exerciseCode += '\n'.repeat(nLF)
    // }
    this.editor.getSession().setValue(exerciseCode);
    if(doSave) this.save(exerciseCode)
  }



  //-------------------------------------------------------------------------


  updateValidationBtnColor(done){
    done ??= this.storage.done
    const color = !done ? "unset" : done<0 ? 'red' : 'green'
    $(`${this.globalIdH} button[btn_kind=check]`).css('--ide-btn-color',  color)
  }



  /**Extract the current content of the given editor, explore it, and toggle all the LOCs
   * found after the `TestToken` token.
   *
   * Rules for toggling or not are:
   *      - leading spaces do not affect the logic.
   *      - comment out if the first non space character is not "#".
   *      - if the first non space char is "#" and there is no spaces after it, uncomment.
   * */
  toggleComments(e) {
    if(e && e.preventDefault) e.preventDefault()

    const codeLines   = this.getCodeToTest().split('\n')
    const pattern     = CONFIG.lang.tests.as_pattern
    const iTestsToken = codeLines.findIndex(s=>pattern.test(s))

    /// No tests found:
    if(iTestsToken<0) return;

    const toggled = codeLines.slice(iTestsToken+1).map(s=>{
        return s.replace(CONFIG.COMMENTED_PATTERN, (_,spaces,head,tail)=>{
            if(head=='#' && tail!=' ') return spaces+tail
            if(head!='#') return spaces+'#'+head+tail
            return _
        })
    })
    codeLines.splice(iTestsToken+1, toggled.length, ...toggled)
    const repl = codeLines.join('\n')
    this.applyCodeToEditorAndSave(repl)
    this.focusEditor()
  }



  /**Download the current content of the editor to the download folder of the user.
   * */
  download(){   jsLogger("[Download]")

    let ideContent = this.getCodeToTest() + "" // enforce stringification in any case
    downloader(ideContent, this.pyName)
    this.focusEditor()
  }


  /**Reset the content of the editor to its initial content, and reset the localStorage for
   * this editor on the way.
   * */
  restart(){    jsLogger("[Restart]")
    this.setAttemptsCounter(this.srcAttemptsLeft)
    const exerciseCode = this.getStartCode()
    this.storage = freshStore(exerciseCode, this)
    this.applyCodeToEditorAndSave(exerciseCode)
    this.updateValidationBtnColor()
    $("#solution_" + this.id).addClass('py_mk_hidden')
    this.hiddenDivContent = true
    this.terminal.clear()
    clearPyodideScope()
    this.focusEditor()
  }



  /**Save the current IDE content of the user, or the given code, into the localStorage
  * of the navigator.
  * */
  save(givenCode=""){   jsLogger("[Save]")
    const currentCode = givenCode || this.getCodeToTest()
    this.setStorage({code: currentCode, hash:this.srcHash})
  }




  playFactory()    { throw new Error("Should be overridden in child class") }
  validateFactory(){ throw new Error("Should be overridden in child class") }



  /**Is the current action "running the public tests"?
   * */
  isPlaying(){  return this.running.includes(CONFIG.runningMode.play) }

  /**Is the current action "running the validation tests"?
   * */
  isChecking(){ return this.running.includes(CONFIG.runningMode.validate) }



  /**Relay method, to transfer stdout content from pyodide to the jQuery.terminal.
   * If @isPrint is true, the call has been done through the `bi_print` python function.
   * If @isPrint is false, then the call has been done through the `terminal_message` function.
   *
   * When the stdout is deactivated and @isPrint is false, the @key argument is required to
   * match the one given through the IDE macro `STD_KEY` argument.
   * */
  termFeedbackFromPyodide(key, msg, format, isPrint=false, newline=undefined){
    const hidden    =  isPrint && !this.allowPrint
    const forbidden = !isPrint && !this.allowPrint && key != this.stdKey
    if(forbidden){
      throw new PythonError("Cannot print to the terminal.")
    }
    if(!(isPrint && hidden)){
      super.termFeedbackFromPyodide(null, msg, format, isPrint, newline ?? !isPrint)
    }
  }
}


















class IdeRunner extends _IdeEditorHandler {



  // @Override
  build(){
    super.build()
    if(this.profile===CONFIG.PROFILES.revealed){
      this.revealSolutionAndRems(true)
    }
  }



  /**Does nothing, but catch any call on the parent class, which would raise an error
   * because prefillTerm is undefined, for IDEs.
   * */
  prefillTermIfAny(){}



  /**The terminal behaves differently when IDE content is run, so must be handled from here.
   * (mostly: through command lines, the terminal content is not cleared).
   *
   *  - If not paused, the terminal automatically displays a new line for a fresh command.
   *  - So clear content only after if got paused.
   *  - Then show to the user that executions started and enforce terminal GUI refresh,
   *    with a tiny pause so that the user has time to see the "cleared" terminal content.
   *  - Then, relay to super setup methods.
   * */
  async setupRuntimeIDE() {
    jsLogger("[CheckPoint] - setupRuntimeIDE IdeRunner")

    this.resizeVerticalTerm()           // needed in case the first click is on a button
    this.terminalAutoWidthOnResize()

    // save before anything else, in case an error occur somewhere...
    const editorCode = this.getCodeToTest()
    this.save(editorCode)
    this.storeUserCodeInPython('__USER_CODE__', editorCode)

    this.terminal.pause()           // Deactivate user actions in the terminal until resumed
    this.terminal.clear()           // To do AFTER pausing...
    this.terminalDisplayOnStart()   // Handle the terminal display for the current action
    await sleep(this.delay)         // Terminal "blink", so that the user always sees a change
    this.alreadyRanEnv = true

    return this.setupRuntime()
  }


  /**Things to display in the terminal at the very beginning of the executions.
   * */
  terminalDisplayOnStart(){
    this.terminalEcho(CONFIG.lang.runScript.msg)
  }



  async teardownRuntimeIDE(runtime) {
    jsLogger("[CheckPoint] - IdeRunner teardownRuntime")

    // Restore default state first, in case a validation occurred (=> restore stdout behaviors!)
    runtime.refreshStateWith()

    // Handle any extra final message (related to revelation of solutions & REMs)
    if(runtime.finalMsg) this.giveFeedback(runtime.finalMsg, null)

    await this.teardownRuntime(runtime)
    this.storeUserCodeInPython('__USER_CODE__', "")
  }



  /**If the current action has been successful until now, display the appropriate
   * message in the terminal.
   * */
  codeSnippetEndFeedback(runtime, step, code){
    if(runtime.stopped || !step) return

    const playing = this.isPlaying()
    const intro   = playing ? "" : CONFIG.lang.validation.msg
    const section = CONFIG.lang[step].msg
    const ok      = CONFIG.lang.successMsg.msg

    let msg = `${ intro }${ section }: ${ ok }`   // Default section message
    if(!code) msg = ""                            // No default message if no code in the section...
    if(playing && !this.hasCheckBtn){             // ...but ensure the default ending message is shown,
      msg = CONFIG.lang.successMsgNoTests.msg     //    if this is "playing" dans nothing else to do after.
    }

    if(msg) this.terminalEcho(msg)

    // If no error yet and secret tests exist while running the public tests right now,
    // prepare a "very final" message reminding to try the validations:
    if(playing && this.hasCheckBtn){
      runtime.finalMsg = CONFIG.lang.unforgettable.msg
    }
  }





  //--------------------------------------------------------------------




  /**Build the public tests runner routine.
   * */
  playFactory(runningMan=CONFIG.runningMode.play){
    return this.lockedRunnerWithBigFailWarningFactory(
      runningMan,
      this.setupRuntimeIDE,
      this.playThroughRunner,
      this.teardownRuntimeIDE,
    )
  }

  /**Build the validation tests runner routine.
   * */
  validateFactory(runningMan=CONFIG.runningMode.validate){
    return this.lockedRunnerWithBigFailWarningFactory(
      runningMan,
      this.setupRuntimeIDE,
      this.validateThroughRunner,
      this.teardownRuntimeIDE,
    )
  }

  /**Build the correction validation runner routine.
   * NOTE: the pyodideLock setup is not correct here (swaps done outside of it), but it shouldn't
   *       ever cause troubles, as long as this method is not used in the IdeTester objects.
   * */
  validateCorrFactory(){
    const cbk = this.validateFactory()
    const wrapper = async (e)=>{
      jsLogger("[CheckPoint] - corr_btn start")

      const codeGetter   = this.getCodeToTest
      const currentEditor= this.getCodeToTest()
      const profile      = this.profile
      this.getCodeToTest = ()=>this.corrContent
      this.data.profile  = null    // REMINDER: getters without setters, so need inner update!

      let out
      try{
        out = await cbk(e)
      }finally{
        jsLogger("[CheckPoint] - corr_btn validation done")
        this.data.profile  = profile
        this.getCodeToTest = codeGetter
        this.save(currentEditor)    // Ensure the corr content doesn't stay stored in localStorage
      }
      return out
    }
    return wrapper
  }




  //--------------------------------------------------------------------




  /** `lockedRunnerWithBigFailWarningFactory(@action)` routine, to run public tests.
   * */
  async playThroughRunner(runtime){
    const code = this.getCodeToTest()
    await this.runPythonCodeWithOptionsIfNoStdErr(code, runtime, CONFIG.section.editor)
  }


  /** `lockedRunnerWithBigFailWarningFactory(@action)` routine, to run validation tests.
   * */
  async validateThroughRunner(runtime){

    // env section is behaving like the editor one (should be changed...?)
    let decrease_count = this.canDecreaseAttempts(CONFIG.section.editor)

    // If an error already occurred, stop everything...
    if(runtime.stopped){

      // ... but decrease the number attempts and run teardown if this was AssertionError.
      if(runtime.isAssertErr){
        this.handleRunOutcome(runtime, decrease_count)
      }

    }else{

      const validation_state = {
        autoLogAssert:    this.autoLogAssert,
        purgeStackTrace:  this.showOnlyAssertionErrorsForSecrets,
        withStdOut:      !this.deactivateStdoutForSecrets,
      }
      const toRun = [
        [this.getCodeToTest(), CONFIG.section.editor,  {}],
        [this.publicTests,     CONFIG.section.public,  validation_state],
        [this.secretTests,     CONFIG.section.secrets, validation_state],
      ]

      for(const [code, testSection, state] of toRun){
        jsLogger("[CheckPoint] - Run validation step:", testSection)

        runtime.refreshStateWith(state)
        await this.runPythonCodeWithOptionsIfNoStdErr(code, runtime, testSection)

        if(runtime.stopped){
          decrease_count = this.canDecreaseAttempts(testSection)
          break
        }
      }

      // Reveal solution and REMs on success, or if the counter reached 0 and the sol&REMs content
      // is still hidden, then prepare an appropriate revelation message if needed (`finalMsg`).
      this.handleRunOutcome(runtime, decrease_count)
    }
  }





  //-----------------------------------------------------------------------







  /**Return true if the current section allow to decrease the number of attempts,
   * during a validation.
   * */
  canDecreaseAttempts(testSection){
    const wanted      = CONFIG.section[ this.decreaseAttemptsOnUserCodeFailure ]
    const allowedFrom = CONFIG.sectionOrder[ wanted ]
    const currentAt   = CONFIG.sectionOrder[ testSection ]
    const canDecrease = currentAt >= allowedFrom
    return canDecrease
  }



  /**Reveal solution and REMs on success, or if the counter reached 0 and the sol&REMs content
   * is still hidden, then prepare an appropriate revelation message if needed (`finalMsg`).
   *
   * Do not forget that any error related feedback has already been printed to the console, so
   * when it comes to feedback given in this method, it's only about a potential "final message".
   * */
  handleRunOutcome(runtime, allowCountDecrease){
    const success      = !runtime.stopped
    const isDelayed    = this.profile === CONFIG.PROFILES.delayedReveal
    const someToReveal = this.corrRemsMask && this.hiddenDivContent && (!this.profile || isDelayed)

    jsLogger("[CheckPoint] - handleRunOutcome")
    // console.log("[OutCome]", JSON.stringify({ success, pof:this.profile, revealable, hidden:this.hiddenDivContent, allowCountDecrease: !!allowCountDecrease, mask:this.corrRemsMask, N:this.attemptsLeft}))

    this.setStorage({done: success ? 1:-1 })
    this.updateValidationBtnColor()

    if(allowCountDecrease && (!success || isDelayed)){
      this.decreaseIdeCounter()
    }

    // Reveal if success and not delayed, or if attempts==0 (means last error, are last delayed)
    const isRevelation =  someToReveal && (success && !isDelayed || this.attemptsLeft===0)

    /*If success, a custom final message has to be built:
          - If the revelation already occurred, return no message at all
          - If some profile forbids the revelation, or if nothing to reveal, just congratulate the user.
          - Make sure a success on "delayed" profile doesn't trigger a final message.

      WARNING: someToReveal is different from "already revealed".
     */
    const isSuccessNoReveal = success && this.hiddenDivContent && !isDelayed

    if(isRevelation){
      jsLogger("[OutCome]", 'reveal!', success)
      runtime.finalMsg = success ? this._buildSuccessMessage(someToReveal, isDelayed)
                                 : this._getSolRemTxt(false)
      this.revealSolutionAndRems()

    }else if(isSuccessNoReveal){
      // Always display the "bravo" message on success, if corr&REMs exist but are not revealable
      runtime.finalMsg = this._buildSuccessMessage(someToReveal, isDelayed)
    }
  }


  /**Decrease the number of attempts left, EXCEPT when:
   *    - the solution is already revealed,
   *    - the number of attempts is infinite,
   *    - there are no attempts left (redundant with revelation condition, but hey...).
   */
  decreaseIdeCounter(){
    jsLogger("[CheckPoint] - decreaseIdeCounter")
    if(!this.hiddenDivContent) return    // already revealed => nothing to change.

    // Allow going below 0 so that triggers once only for failure.
    const nAttempts = Math.max(-1, this.attemptsLeft - 1)

    // Update the GUI counter if needed (check for encryption in case
    // the user already solved the problem)
    if(Number.isFinite(nAttempts) && nAttempts >= 0){
      this.setAttemptsCounter(nAttempts)
    }
  }


  setAttemptsCounter(nAttempts){
    this.data.attempts_left = nAttempts
    $(this.counterH).text(nAttempts)
  }


  /**Reveal corr and/or REMs (visible or not) contents.
   * When reaching this method, it is already sure by contract, that the revelation must occur.
   * The only piece of contract this method is holding is that if flags the revelation as done,
   * and it decides if the div content has to be decompressed or not on the way.
   * */
  revealSolutionAndRems(waitForMathJax=false){
    jsLogger("[CheckPoint] - Enter revealSolutionAndRems")
    // Need to check here one more time against hiddenDivContent because of the "show" button logic.
    if(this.hiddenDivContent){
      jsLogger("[CheckPoint] - revealed!")

      const sol_div = $("#solution_" + this.id)

      if(this.isEncrypted){
        const compressed = sol_div.text().trim()
        const content    = compressed && decompressLZW(compressed, "ides.encrypt_corrections_and_rems")
        sol_div.html(content)
        this.data.is_encrypted = false  // Never decompress again
      }
      sol_div.attr('class', '')         // Unhide
      this.hiddenDivContent = false     // Never reveal agin (last in case of errors...)

      // Enforce formatting
      if(waitForMathJax){
        subscribeWhenReady(
          "revealOnLoad", mathJaxUpdate, {runOnly:true, waitFor:()=>CONFIG.subscriptionReady.mathJax}
        )
      }else{
        mathJaxUpdate()
      }

      /* DOESN'T WORK
      // Enforce mermaid rendering if any
      try{
        // Need to make an async call, but i don't want to make this method an async one...
        setTimeout(async ()=>console.log('yup?') || await mermaid.run())
      }catch(e){}
      //*/
    }
  }


  /**If @isDelayed is true, there are no tests/secrets, so:
   *    - Do not congratulate the user
   *    - if something revealable, announce the revelation, otherwise say nothing special
   *
   * If @isDelayed is false, build:
   *    - the complete success message if something to reveal
   *    - only the bravo message otherwise.
   */
  _buildSuccessMessage(revealable, isDelayed){
    const moreInfo = revealable ? this._getSolRemTxt(true) : ""
    if(isDelayed){
      return moreInfo && txtFormat.stress(moreInfo)
    }
    const emo = choice(CONFIG.MSG.successEmojis)
    return `${ CONFIG.lang.successHead.msg } ${ emo } ${ CONFIG.lang.successHeadExtra.msg }${ moreInfo }`
  }


  _getSolRemTxt(isSuccess){
    if(!this.corrRemsMask) return ""

    const hasCorr  = this.corrRemsMask & 1
    const hasRems  = this.corrRemsMask & 2
    const hasBoth  = this.corrRemsMask == 3
    const msg      = []
    const sentence = []

    const pushSentence = (prop, kind='msg') => sentence.push(CONFIG.lang[prop][kind])

    msg.push(
      isSuccess ? "\n"+CONFIG.lang.successTail.msg
                : CONFIG.lang.failHead.msg
    )

    if(hasCorr) pushSentence('revealCorr')
    if(hasBoth) pushSentence('revealJoin')
    if(hasRems) pushSentence('revealRem')

    if(!isSuccess){
        if(sentence.length) sentence[0] = _.capitalize(sentence[0])

        if(hasBoth||hasRems) pushSentence('failTail', 'plural')
        else                 pushSentence('failTail')
    }
    msg.push(...sentence)
    const output = msg.join(' ').trimEnd() + "."

    // console.log("[OutComeSolRemTxt]", JSON.stringify({isSuccess, msg, mask:this.corrRemsMask, sentence, output}))
    return output
  }
}

CONFIG.CLASSES_POOL.Ide = IdeRunner
