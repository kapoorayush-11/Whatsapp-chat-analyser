import streamlit as st
import preprocessor 
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    ## To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    ## converting the byte data into text(utf-8 decoding)
    data = bytes_data.decode('utf-8')
    #st.text(data)  # Displaying it on app
    df = preprocessor.preprocess(data)
    
    #st.dataframe(df)                          # This is the message dataframe which is right now I'm not showing.
    
    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    
    selected_user=st.sidebar.selectbox('Show analysis for',user_list)
    
    
    #Let's add a button to show analysis
    if st.sidebar.button('Show Analysis'):
        
        num_messages,words,num_media_msg,num_links = helper.fetch_stats(selected_user,df)
        
        col1,col2,col3,col4 = st.columns(4)
        
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_msg)
        with col4:
            st.header('Links Shared')
            st.title(num_links)
        
    # Timeline of conversations
        
        #Monthly timeline
        st.title('Timelines')
        col1,col2 = st.columns(2)
        
        with col1:
            timeline = helper.monthly_timeline(selected_user, df)
            st.header('Monthly Timeline')
            fig,ax = plt.subplots()
            ax.plot(timeline['time'],timeline['message'])
            plt.xticks(rotation =37)
            st.pyplot(fig)
        
        #Daily Activity
        with col2:
            st.header("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation=37)
            st.pyplot(fig)
            
        
        #Activity Maps
        st.title('Activity Map')
        col1,col2= st.columns(2)
        
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation=37)
            st.pyplot(fig)
        
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
    
   # Finding most busy user(group level)
        
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,busy_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()
            
            col1,col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values,color='red')
                #plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(busy_df)
                
       
    # Wordcloud
        st.title('Wordcloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
    #Most Common Words
        st.title('Most Common Words')
        most_common_df=helper.most_common_words(selected_user, df)
        
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation=60)
        st.pyplot(fig)
                

            
            
            
            
            
            
            
            
            
            