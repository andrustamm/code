# components/tab8_category_rules.py
import streamlit as st
import config

def render():
    st.header("Kategooriate reeglite haldamine")
    st.caption("Siin saad muuta teenuste ja kulumudelite märksõnade vastendamise reegleid.")

    # Initialize state from file if not already present
    if "category_rules" not in st.session_state:
        st.session_state.category_rules = config.load_category_rules()

    rules = st.session_state.category_rules.copy()

    st.subheader("Olemasolevad kategooriad ja märksõnad")
    
    updated_rules = {}
    categories_to_delete = []

    # Display an editor card/row for each category
    for cat_name, keywords in rules.items():
        col1, col2, col3 = st.columns([2, 5, 1])
        
        with col1:
            st.markdown(f"**{cat_name}**")
            
        with col2:
            # Convert list of keywords to comma-separated text input
            current_kw_str = ", ".join(keywords)
            new_kw_str = st.text_input(
                f"Märksõnad ({cat_name})",
                value=current_kw_str,
                key=f"kw_{cat_name}",
                label_visibility="collapsed"
            )
            # Parse input back into list
            parsed_keywords = [kw.strip() for kw in new_kw_str.split(",") if kw.strip()]
            updated_rules[cat_name] = parsed_keywords

        with col3:
            if st.button("Kustuta", key=f"del_{cat_name}", type="secondary"):
                categories_to_delete.append(cat_name)

    # Process deletions
    for cat in categories_to_delete:
        if cat in updated_rules:
            del updated_rules[cat]
            st.session_state.category_rules = updated_rules
            st.rerun()

    st.markdown("---")

    # Add a new category
    st.subheader("Lisa uus kategooria")
    with st.form("add_category_form", clear_on_submit=True):
        col_new_name, col_new_kw = st.columns([2, 5])
        with col_new_name:
            new_cat_name = st.text_input("Kategooria nimi", placeholder="nt. Muud teenused")
        with col_new_kw:
            new_cat_kws = st.text_input("Märksõnad (komadega eraldatud)", placeholder="nt. lisateenus, kuutasu")
        
        add_submitted = st.form_submit_button("Lisa kategooria")
        
        if add_submitted:
            if not new_cat_name.strip():
                st.error("Kategooria nimi ei saa olla tühi!")
            elif new_cat_name in updated_rules:
                st.warning("See kategooria on juba olemas!")
            else:
                parsed_kws = [k.strip() for k in new_cat_kws.split(",") if k.strip()]
                updated_rules[new_cat_name] = parsed_kws
                st.session_state.category_rules = updated_rules
                st.success(f"Kategooria '{new_cat_name}' lisatud!")
                st.rerun()

    # Save button for updating the file
    st.markdown("---")
    if st.button("Salvesta muudatused faili", type="primary"):
        if config.save_category_rules(updated_rules):
            st.session_state.category_rules = updated_rules
            # Reload global CATEGORY_RULES in config
            config.CATEGORY_RULES = updated_rules
            st.success("Reeglid edukalt salvestatud faili `data/category_rules.json`!")
        else:
            st.error("Viga reeglite salvestamisel faili.")