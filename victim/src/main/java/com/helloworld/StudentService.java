package com.helloworld;

import org.springframework.data.domain.Page;
import java.util.List;

public interface StudentService {
    List<Student> getAllStudents();
    void saveStudent(Student student);
    Student getStudentById(long id);
    void deleteStudentById(long id);
    Page<Student> findPaginated(int pageNum, int pageSize, String sortField, String sortDirection);
}
