# dashboard.py
import streamlit as st
import pandas as pd
#import seaborn as sns
import plotly.express as px

# Load the "mpg.csv" dataset
df = pd.read_csv('mpg.csv')

# Function to display dataset information
def show_dataset_info():
    st.subheader("Dataset Information")
    st.write("Number of Rows: " + str(df.shape[0]))
    st.write("Number of Columns: " + str(df.shape[1]))
    st.write("Missing Values:")
    st.write(df.isnull().sum())

# Function to display the dataset in a table
def show_data_table():
    st.subheader("Data Table")
    st.dataframe(df)

# Function to display a bar chart for origin
def show_origin_chart():
    origin_count = df['origin'].value_counts()
    st.subheader("Origin-wise Distribution")
    fig = px.bar(origin_count, x=origin_count.index, y=origin_count.values, labels={'x': 'Origin', 'y': 'Count'})
    st.plotly_chart(fig)

# Function to display bar graphs
def show_bar_graph():
    st.subheader("Bar Graph")
    
    # Select variables for the bar graph
    x_variable = st.selectbox("Select X-axis Variable", df.columns, key=hash("x"))
    y_variable = st.selectbox("Select Y-axis Variable", df.columns, key=hash("y"))
    
    # Create the bar graph
    fig = px.bar(df, x=x_variable, y=y_variable, title=f"{x_variable} vs {y_variable} Bar Graph")
    
    # Add axis labels
    fig.update_layout(
        xaxis_title=x_variable,
        yaxis_title=y_variable,
    )
    
    st.plotly_chart(fig)


# Function to show data filters and display filtered data table
def show_data_filters():
    st.subheader("Data Filters")
    
    # Select the variable for filtering
    selected_variable = st.selectbox("Select a Variable for Filtering", df.columns)
    
    # Set the filtering conditions
    filter_min = st.slider(f"Select Minimum Value for {selected_variable}", float(df[selected_variable].min()), float(df[selected_variable].max()), float(df[selected_variable].min()))
    filter_max = st.slider(f"Select Maximum Value for {selected_variable}", float(df[selected_variable].min()), float(df[selected_variable].max()), float(df[selected_variable].max()))

    # Apply the filtering
    filtered_data = df[(df[selected_variable] >= filter_min) & (df[selected_variable] <= filter_max)]
    
    st.subheader("Filtered Data Table")
    st.dataframe(filtered_data)

# Function to display scatter plots
def show_scatter_plots():
    st.subheader("Scatter Plots")
    
    # Select variables for the scatter plot
    x_variable = st.selectbox("Select X-axis Variable", df.columns)
    y_variable = st.selectbox("Select Y-axis Variable", df.columns)
    
    # Create the scatter plot
    fig = px.scatter(df, x=x_variable, y=y_variable, hover_name="car name", title=f"{x_variable} vs {y_variable} Scatter Plot")
    
    # Add axis labels
    fig.update_layout(
        xaxis_title=x_variable,
        yaxis_title=y_variable,
    )
    
    st.plotly_chart(fig)


# Function to display line plot with average Y-axis
def show_line_plot():
    st.subheader("Line Plot with Average")
    
    # Set the 'model year' column as the index
    df_indexed = df.set_index('model year')
    
    # Select variables for the line plot
    x_variable = 'model year'
    y_variable = st.selectbox("Select Y-axis Variable", df.columns, key=hash("y_var"))
    
    # Calculate the average of the Y-axis variable for each unique value of the X-axis variable
    avg_data = df_indexed.groupby(x_variable)[y_variable].mean().reset_index()
    
    # Create the line plot
    fig = px.line(avg_data, x=x_variable, y=y_variable, markers=True, title=f"{x_variable} vs Average {y_variable}")
    
    # Add axis labels
    fig.update_layout(
        xaxis_title=x_variable,
        yaxis_title=f"Average {y_variable}",
    )
    
    st.plotly_chart(fig)



# Function to display a histogram
def show_histogram():
    st.subheader("Histogram")
    
    # Select the variable for the histogram
    selected_variable = st.selectbox("Select a Numeric Variable", df.select_dtypes(include='number').columns)
    
    # Create the histogram
    fig = px.histogram(df, x=selected_variable, nbins=20, title=f"Histogram of {selected_variable}")
    
    # Add axis labels
    fig.update_layout(
        xaxis_title=selected_variable,
        yaxis_title="Frequency",
    )
    
    st.plotly_chart(fig)

# Function to display pie chart with selected column
def show_pie_chart():
    st.subheader("Pie Chart")
    
    # List of columns you want to include in the pie chart
    columns_for_pie_chart = ['model year', 'origin', 'cylinders']  
    
    # Select the variable for the pie chart from the predefined list
    selected_variable = st.selectbox("Select a Variable for Pie Chart", columns_for_pie_chart)
    
    # Calculate the counts for each category in the selected variable
    pie_data = df[selected_variable].value_counts()
    
    # Create the pie chart
    fig = px.pie(pie_data, names=pie_data.index, values=pie_data.values, title=f"Pie Chart for {selected_variable}")
    
    st.plotly_chart(fig)

# Function to add a filter by year button to the dashboard
def filter_by_year_button():
    st.subheader("Filter by Year Button")
    button_clicked = st.button("Filter by Year")
    if button_clicked:
        selected_year = st.slider("Select Year", int(df['model year'].min()), int(df['model year'].max()))
        filtered_data = df[df['model year'] == selected_year]
        st.dataframe(filtered_data)

# Function to add a date input for specific date to the dashboard
def specific_date_input():
    st.subheader("Specific Date Input")
    selected_date = st.date_input("Select a Specific Date")
    specific_data = df[df['date'] == selected_date.strftime('%Y-%m-%d')]
    st.dataframe(specific_data)

# Function to add a radio button to filter by cylinders to the dashboard
def filter_by_cylinders_radio():
    st.subheader("Filter by Cylinders Radio Button")
    options = st.radio("Select Number of Cylinders", sorted(df['cylinders'].unique()))
    filtered_data = df[df['cylinders'] == options]
    st.dataframe(filtered_data)

# Function to add a checkbox to filter by origin to the dashboard
def filter_by_origin_checkbox():
    st.subheader("Filter by Origin Checkbox")
    selected_origin = st.checkbox("American Origin")
    if selected_origin:
        filtered_data = df[df['origin'] == 'america']
    else:
        filtered_data = df[df['origin'] != 'america']
    st.dataframe(filtered_data)



def main():
    st.title("MPG Dataset Dashboard")
    st.write("Explore the dataset interactively using the options below.")

    # Display dataset info and basic statistics
    show_dataset_info()

    # Display the dataset in a table
    show_data_table()

    # Display origin-wise distribution chart
    show_origin_chart()

    #Display bargraph
    show_bar_graph()

    # Show data filters and filtered data table
    show_data_filters()

    # Display scatter plots
    show_scatter_plots()

    # Display line plot with average Y-axis
    show_line_plot()

    # Display histogram
    show_histogram()

    # Display pie chart
    show_pie_chart()

    filter_by_year_button()
    specific_date_input()
    filter_by_cylinders_radio()
    filter_by_origin_checkbox()


if __name__ == "__main__":
    main()


