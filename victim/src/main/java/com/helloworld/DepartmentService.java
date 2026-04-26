package com.helloworld;

import org.springframework.data.domain.Page;
import java.util.List;

public interface DepartmentService {
    List<Department> getAllDepartments();
    void saveDepartment(Department department);
    Department getDepartmentById(long id);
    void deleteDepartmentById(long id);
    Page<Department> findPaginated(int pageNum, int pageSize, String sortField, String sortDirection);
}
