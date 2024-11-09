def short_word_treatment(text,add_words=None,remove_words=None,remove_all=False,text_case='same'):
    '''
    ABOUT:
        This function processes an input text by expanding commonly used short words, acronyms, and abbreviations
        into their full forms. It leverages a predefined dictionary of common short words and their expansions
        while providing flexibility for customization. Users can add their own short words, remove specific short words,
        or clear the entire predefined list to use only their custom definitions. The function also allows adjusting
        the case of the output text to match specific needs, making it a versatile tool for text normalization
        in various applications such as chat processing, text analysis, and more.

    PARAMETERS:
        * text (str):
             The input text to be processed.

        * add_words (dict, optional):
             A dictionary containing custom short words as keys and their corresponding full forms as values.
             These custom short words will be added to the predefined vocabulary of short words.
             Default is None.

        * remove_words (list, optional):
             A list of short words to be removed from the predefined vocabulary. Default is None.

        * remove_all (bool, optional):
             If True, the function will clear the predefined vocabulary of short words, allowing only user-defined short words to be used.
             Default is False.

        * text_case (str, optional):
             Specifies the case of the returned text. Options are:
             - 'same': Retains the original case of the text (default).
             - 'lower': Converts the text to lowercase.
             - 'upper': Converts the text to uppercase.

    RETURNS:
        str: The processed text with short words expanded into their full forms.

    EXAMPLE USAGE:
        >>> input_text = "OMG, BTW IRL, JK! LOL"
        >>> expanded_text = short_word_treatment(input_text)
        >>> print(expanded_text)
        "Oh my God, By the way In real life, Just kidding! Laugh out loud"

        >>> custom_words = {'FYI': 'For your information', 'BRB': 'Be right back'}
        >>> input_text = "FYI, I'll BRB"
        >>> expanded_text = short_word_treatment(input_text, add_words=custom_words)
        >>> print(expanded_text)
        "For your information, I'll Be right back"

        >>> input_text = "LOL, I'll BRB"
        >>> expanded_text = short_word_treatment(input_text, remove_words=['LOL'])
        >>> print(expanded_text)
        "LOL, I'll Be right back"

        >>> input_text = "OMG, I can't believe it!"
        >>> expanded_text = short_word_treatment(input_text, remove_all=True, add_words={'OMG': 'Oh my goodness'})
        >>> print(expanded_text)
        "Oh my goodness, I can't believe it!"

        >>> input_text = "OMG, this is awesome!"
        >>> expanded_text = short_word_treatment(input_text, text_case='upper')
        >>> print(expanded_text)
        "OH MY GOD, THIS IS AWESOME!"

    NOTES:
        - If you wish to retain only a few short words, you can achieve that through parameter tuning by using
          `remove_all=True` and `add_words` to specify only the desired short words.
        - The function can handle punctuation and special characters effectively, ensuring that only actual short words
          are expanded while preserving the overall structure and meaning of the text.
        - It maintains consistency with the input text's style and punctuation.
        - The function is designed to be robust and handle common exceptions, such as missing or incorrect parameters,
          gracefully.
    '''

    wt=[]
    try:

      import warnings
      warnings.filterwarnings('ignore')

      d={'LOL': 'Laugh out loud',
      'BRB': 'Be right back',
      'OMG': 'Oh my God',
      'TTYL': 'Talk to you later',
      'BTW': 'By the way',
      'SMH': 'Shaking my head',
      'IMO': 'In my opinion',
      'FYI': 'For your information',
      'JK': 'Just kidding',
      'ROFL': 'Rolling on the floor laughing',
      'NP': 'No problem',
      'TMI': 'Too much information',
      'ASAP': 'As soon as possible',
      'GTG': 'Got to go',
      'IMO': 'In my opinion',
      'AFK': 'Away from keyboard',
      'NVM': 'Never mind',
      'OP' : 'Over power',
      'ILU': 'I love you',
      'BC' : 'Because',
      'DM' : 'Direct message',
      'FTW': 'For the win',
      'IDK': "I don't know",
      'IRL': 'In real life',
      'LMK': 'Let me know',
      'NBD': 'No big deal',
      'SU' : 'Shut up',
      'THX': 'Thanks',
      'ST' : 'Stop talking',
      'YOLO':'You only live once',
      'WTH' :'What the hack',
      'GL' : 'Good luck',
      'BOL':'Best of luck',
      'OMW': 'On my way',
      'IDC': "I don't care",
      'TBH': 'To be honest',
      'IWB': 'I will be back',
      'OTW': 'On the way',
      'U'  : 'You',
      'WKLY':'Weekly',
      'COMP':'Competition',
      'R'  : 'Are',
      'TBH': 'To be honest','CAJ':'Casual','OFC':' Of course','TBF':'To be fair','IKR':'I know, right','STFU':'Shut the fuck up','TMB':'Text me back',
      'R8' : 'Right','SRY':'Sorry','GJ':'Good job','W8AM':' Wait a minute','PIC':'Picture','KK':'Okay cool','GM':'Good morning','L8R':'Later',
      'BBL':'Be back later','SEC':'Second','NC':'No comment','B4':'Before','BB':'Bye bye','XOXO':'Hugs and kisses','IMO':'In my opinion','ZZZ':'Sleeping',
      'JJ':'Just joking','F2F':'Face to face','CU':'See you','FAB':'Fabulous','TXT':'Text','M8':'Mate','DND':'Do not disturb','ILY':'I love you',
      'Q4U':'Question for you','TYT':'Take your time','LMA':'Leave me alone','5N':'Fine','Tho':'Though','AFAIK':'As far as I know','BFF':'Best friends forever',
      'FOMO':'Fear of missing out','ICYMI':'In case you missed it','NM':'Not much','OMW':'On my way','OTOH':'On the other hand','IG':'Instagram',
      'JIC':'Just in case','FB':'Facebook','WBU':'What about you','WFH':'Work from home','TYVM':'Thank you very much','WYA':'Where you at',
      'MSG':'Message','DIY':'Do it yourself','BFN':'Bye for now','EOD':'End of day','GOAT':'Greatest of all time','EZ':'Easy','NOYB':'None of your business',
      'SRSLY':'Seriously','VS':'Versus','FBO':'Facebook official','SRS':'Serious','2DAY':'today','2MORO':'Tomorrow','GR8':'Great','ILU2':'I love you too',
      'HR':'Human resources','F2F':'Face to face','WTF':'What the fuck','CYA':'See you'}

      if type(text) != str:
        raise TypeError("text must be a string")
      elif type(text) == str:
        text2=text
      a=0
      c='Pre'
      df=0
      data=0
      df_sorted=0
      short=[]
      w=[]
      d1=[]
      ddd=[]
      sp_word=[]
      sp_word1=[]
      sp_word2=[]

      if remove_all == True:
        d.clear()
      elif remove_all not in(True,False):
        raise ValueError("remove_all must be either True or False")

      if add_words != None and type(add_words) == dict:
          #d1={f1:f2 for f1,f2 in zip(word,full_form)}
          for i,j in add_words.items():
              d[i.upper()]=j
      elif add_words != None and type(add_words) != dict:
          raise TypeError("add_words must be a dictionary")

      if remove_words != None and type(remove_words) in(list,tuple,set):
          for k in remove_words:
              d.pop(k.upper())
      elif remove_words != None and type(remove_words) not in(list,tuple,set):
          raise TypeError("remove_words must be a list, tuple, or set object")

      pun=["!","'",'"',"#","$","%","&","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","|","~","\\"]
      alphabate_list1=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                  'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

      for t in text:
        if t not in pun and t not in alphabate_list1:
          pun.append(t)


      #print(wt)

      def pun_rec(word,punc_list):
          for i in word:
            if i in punc_list:
              word=word.replace(i,' ' + i + ' ')
          return word
          for i2 in word:
            if i2 not in(pp):
              word1=word
          return word1

      #for i in pun:
        #text=text.replace(i, ' ' + i + ' ')

      def short(word,dict1):
        w_list=[]
        alphabate_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                  'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        def case_decode(word,list):
          if word[0] in alphabate_list[0:26]:
            return "upper"
          else:
            return "lower"
        for w in word.split():
          if w.upper() in dict1 and case_decode(w,alphabate_list) == 'lower':
            w_list.append(dict1[w.upper()].lower())
          elif w.upper() in dict1 and case_decode(w,alphabate_list) == 'upper':
            w_list.append(dict1[w.upper()].capitalize())
          else:
            w_list.append(w)
        return ''.join([q for q in w_list])

      text1=text2
      for z in text1.split():
            ddd.append(z)
      #print(wt)
      #print(wt)
      for i in ddd:
        wo=pun_rec(i,pun)
        sp_word.append(wo)
      for i1 in sp_word:
        wo1=short(i1,d)
        sp_word1.append(wo1)

      tx_list=[]
      text11=' '.join([www for www in sp_word1])
      #for tx in text1.split():
        #if tx in pun:
          #tx_list.append(pun12[tx])
      #print(tx_list)
      #for tx1 in tx_list:
          #text1=text1.replace(tx1,pun11[tx1])
          #text1=text1.replace(pun12[tx],pun11[tx])
      #print(text11)

      if text_case=='same':
        return text11
      elif text_case=='lower':
        text22=text11.lower()
        return text22
      elif text_case=='upper':
        text22=text11.upper()
        return text22
      elif text_case not in('same','upper','lower'):
        raise ValueError("text_case value can be ether 'same', 'upper' or 'lower'")
      #return text2
    except ImportError as ip:
      print(ip)

    #except TypeError as ts:
      #print(ts)
    except NameError as ns:
      print(ns)
