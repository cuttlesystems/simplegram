from aiogram.dispatcher import FSMContext

async def ban_user_by_age(state: FSMContext):
    print('we ban user')
    # id, name, gender, age, _, _ = await get_data(state=state)    
    # response = await create_user({
    #     '_id': id,
    #     'name': name,
    #     'gender': gender,
    #     'age': age,
    #     'status': 'too_young'
    # })

    await state.finish()
    return {}